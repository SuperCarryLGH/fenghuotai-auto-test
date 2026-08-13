#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老数据库(yihuishou) → dev 影子表 数据迁移脚本

迁移范围（按手机号过滤已存在用户，同手机号取最新 MAX(id)）：
    sys_user(role_id=5)        → shadow_member_user
    wallet                     → shadow_pay_wallet
    wallet(老库余额>0)          → shadow_pay_wallet_transaction（按钱包各生成一条 increase 流水）
    user_address               → shadow_member_address

关键设计：
  - 关联键：老库 wallet.owner_id / user_address.account_id 引用的是 sys_user.account_id(UUID)，
    因此按 account_id 关联（by_account 映射），不是 sys_user.id
  - 影子表结构与 dev 完全一致；未映射列按 dev 约定填（string→''，int→0，可空列→NULL）
  - 余额单位换算：老库为元(可带小数)，dev 为分 → ×100 (round)
  - 流水：不再读老库 wallet_log；对老库余额>0 的钱包各生成一条
    biz_type=1(收入) 的流水，price=老库余额、balance=dev现有+老库余额
  - ID 生成：与 dev 同构的 snowflake（epoch 1288834974657，<<22）19 位
  - 新用户全量 INSERT(新 ID)；已存在用户：钱包余额累加(dev现有+老)、无目标钱包则新建、
    流水/地址继承现有 user_id/wallet_id
  - 分批(默认5000) + 断点续传 + 重跑前完整性校验
  - 目标依赖：DEP_SOURCE=db 连 dev / xlsx 读线上导出文件

用法：
    python scripts/migrate_old_db_to_shadow.py --init        # 只建影子表
    python scripts/migrate_old_db_to_shadow.py --reset       # 清空影子表+状态
    python scripts/migrate_old_db_to_shadow.py               # 执行迁移（可断点续跑）
    python scripts/migrate_old_db_to_shadow.py --limit 5000  # 试运行：最新5000用户及关联数据
    python scripts/migrate_old_db_to_shadow.py --check       # 查看影子表行数
"""
import json
import os
import random
import re
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pymysql import connect  # noqa: E402
from pymysql.cursors import DictCursor  # noqa: E402

# ============================================================
# 配置区
# ============================================================
OLD_DB = {
    "host": os.getenv("OLD_DB_HOST", "rm-bp1kmprsfdog024fsro.mysql.rds.aliyuncs.com"),
    "port": int(os.getenv("OLD_DB_PORT", "3306")),
    "user": os.getenv("OLD_DB_USER", "xinxibu"),
    "password": os.getenv("OLD_DB_PASSWORD", "Z5eP@E69hGu5xUA"),
    "database": os.getenv("OLD_DB_DATABASE", "yihuishou"),
}
DEV_DB = {
    "host": os.getenv("DB_HOST", "rm-bp1kmprsfdog024fsro.mysql.rds.aliyuncs.com"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "sf_fht_dev"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_DATABASE", "fht_yhs"),
}

DEP_SOURCE = "xlsx"          # "db"=连 dev / "xlsx"=读线上导出文件
XLSX_FILE = "/Users/rs/Documents/online.xlsx"       # 线上导出：单文件双 sheet
XLSX_SHEET_USER = "member_user"                     # 用户表 sheet（列=member_user 字段）
XLSX_SHEET_WALLET = "pay_wallet"                    # 钱包表 sheet（列=pay_wallet 字段）

TENANT_ID = 1
BATCH = 20000
PHONE_RE = r"^1[0-9]{10}$"   # 手机号过滤（老库 phone 可能是设备id）
STATE_FILE = PROJECT_ROOT / "scripts" / ".migrate_state.json"

SHADOW_TABLE = {
    "member_user": "shadow_member_user",
    "pay_wallet": "shadow_pay_wallet",
    "pay_wallet_transaction": "shadow_pay_wallet_transaction",
    "member_address": "shadow_member_address",
}

# 影子表字段对齐线上表：建表后 DROP 线上没有的列（线上 member_user 48 列、pay_wallet 13 列）
_DROP_COLS = {
    "member_user": [
        "customer_type", "biz_type", "auth_id", "auth_company_name", "auth_tax_number",
        "auth_legal_person", "auth_legal_person_phone", "auth_legal_person_id_card",
        "auth_company_province_code", "auth_company_city_code", "auth_company_district_code",
        "auth_company_province", "auth_company_city", "auth_company_district",
        "auth_company_street", "auth_company_detail_address",
        "auth_real_name", "auth_id_card", "auth_status",
    ],
    "pay_wallet": ["deposit_price"],
    "pay_wallet_transaction": [],
    "member_address": [],
}
# ============================================================

# 未映射列的填充值（影子表结构与 dev 完全一致，NOT NULL/默认列按 dev 约定填；可空列留 NULL）
UNMAPPED_FILL = {
    "member_user": {
        "register_ip": "", "login_ip": "", "wx_transfer_openid": "",
        "ali_transfer_name": "", "ali_transfer_mobile": "", "ali_transfer_openid": "",
        "risk_level": 0, "risk_status": 0, "point": 0, "experience": 0,
        "level_id": 1,
    },
    "pay_wallet": {"total_expense": 0, "total_recharge": 0, "freeze_price": 0},
    "pay_wallet_transaction": {"trade_channel": None},
    "member_address": {},
}

_UNMAPPED_COLS = {
    "member_user": [
        "register_ip", "register_terminal", "login_ip", "login_date", "area_id",
        "birthday", "mark", "point", "tag_ids", "level_id", "experience", "group_id",
        "platform", "superior_promoter_id", "super_superior_promoter_id",
        "warehouse_id", "operation_center_id", "scene", "risk_status", "risk_level",
        "wx_transfer_openid", "ali_transfer_name", "ali_transfer_mobile", "ali_transfer_openid",
        "block_reason", "provider",
    ],
    "pay_wallet": ["total_expense", "total_recharge", "freeze_price"],
    "pay_wallet_transaction": ["biz_type", "biz_id", "trade_channel"],
    "member_address": [],
}


def fill_unmapped(table, m):
    """按 dev 约定填充未映射列：有填充值用填充值（NOT NULL 列必须给值），否则 NULL（可空列）"""
    for c in _UNMAPPED_COLS[table]:
        m.setdefault(c, UNMAPPED_FILL.get(table, {}).get(c))

_used_ids = set()

# snowflake
_SNOWFLAKE_EPOCH = 1288834974657   # 2010-11-04
_SNOWFLAKE_WORKER = 0               # dev 未用的 worker 位段（10位）
_SNOWFLAKE_SEQ = 0
_SNOWFLAKE_LAST_MS = 0


def gen_id():
    """与 dev 同构的 snowflake：((ms-epoch)<<22) | (worker<<12) | seq，19位 bigint"""
    global _SNOWFLAKE_SEQ, _SNOWFLAKE_LAST_MS
    for _ in range(100):
        now_ms = int(time.time() * 1000)
        if now_ms != _SNOWFLAKE_LAST_MS:
            _SNOWFLAKE_SEQ = 0
            _SNOWFLAKE_LAST_MS = now_ms
        else:
            _SNOWFLAKE_SEQ += 1
        if _SNOWFLAKE_SEQ >= 4096:          # 同 ms 序列耗尽 → 等待下 1ms
            time.sleep(0.001)
            continue
        nid = ((now_ms - _SNOWFLAKE_EPOCH) << 22) | (_SNOWFLAKE_WORKER << 12) | _SNOWFLAKE_SEQ
        if nid not in _used_ids:
            _used_ids.add(nid)
            return nid
    raise RuntimeError("gen_id 连续碰撞")


def preload_used_ids(dev_conn):
    """预加载 dev 真实表 + 影子表现有 ID 到 _used_ids，确保生成值不与任何已有 ID 冲突"""
    cur = dev_conn.cursor()
    for t in list(SHADOW_TABLE.values()) + ["member_user", "pay_wallet",
                                            "pay_wallet_transaction", "member_address"]:
        try:
            cur.execute(f"SELECT id FROM `{t}`")
        except Exception:
            continue
        for r in cur.fetchall():
            _used_ids.add(int(r["id"]))


def check_id_collision(dev_conn, auto_fix=True):
    """核对影子 ID 是否与 dev 真实表 / 线上 xlsx 的 ID 冲突；冲突则自动重分配并级联引用"""
    cur = dev_conn.cursor()
    shadow_ids = {}
    for key, table in SHADOW_TABLE.items():
        cur.execute(f"SELECT id FROM `{table}`")
        shadow_ids[key] = {int(r["id"]) for r in cur.fetchall()}

    # 禁止集合：dev 真实表 + 线上 xlsx（DEP_SOURCE=xlsx 时）
    forbidden = set()
    online_user_ids = set()          # 线上用户 id（判断"已存在用户继承的线上钱包id"）
    for t in ["member_user", "pay_wallet", "pay_wallet_transaction", "member_address"]:
        cur.execute(f"SELECT id FROM `{t}`")
        forbidden |= {int(r["id"]) for r in cur.fetchall()}
    if DEP_SOURCE == "xlsx":
        import pandas as pd
        try:
            xu = pd.read_excel(XLSX_FILE, sheet_name=XLSX_SHEET_USER, usecols=["id"])
            xw = pd.read_excel(XLSX_FILE, sheet_name=XLSX_SHEET_WALLET, usecols=["id"])
            forbidden |= {int(x) for x in xu["id"].dropna()}
            forbidden |= {int(x) for x in xw["id"].dropna()}
            online_user_ids = {int(x) for x in xu["id"].dropna()}
        except Exception as e:
            print(f"  ⚠️ [collision] 读取 xlsx 失败: {e}")

    # 全部影子 + 禁止 ID 加入 _used_ids，保证重分配不撞
    all_shadow = set()
    for ids in shadow_ids.values():
        all_shadow |= ids
    for x in all_shadow | forbidden:
        _used_ids.add(int(x))

    collisions = {k: (ids & forbidden) for k, ids in shadow_ids.items()}
    collisions = {k: v for k, v in collisions.items() if v}
    # 已存在用户继承的线上钱包 id：user_id 是线上用户 → 有意继承，不算冲突
    if online_user_ids and collisions.get("pay_wallet"):
        hit = collisions["pay_wallet"]
        fmt = ",".join(["%s"] * len(hit))
        cur.execute(f"SELECT id, user_id FROM shadow_pay_wallet WHERE id IN ({fmt})", list(hit))
        inherited = {int(r["id"]) for r in cur.fetchall() if int(r["user_id"]) in online_user_ids}
        collisions["pay_wallet"] = hit - inherited
        collisions = {k: v for k, v in collisions.items() if v}
    total = sum(len(v) for v in collisions.values())

    if not total:
        print("  ✅ [collision] 影子 ID 与 dev真实/线上xlsx 无冲突")
        return True

    print(f"  ⚠️ [collision] 发现冲突 {total} 个:")
    for key, hit in collisions.items():
        print(f"    {SHADOW_TABLE[key]}: {len(hit)} 个（示例 {sorted(hit)[:3]}）")
    if not auto_fix:
        return False

    # 重分配顺序：member_user（级联 钱包/地址）→ pay_wallet（级联 流水）→ 其余
    for key in ["member_user", "pay_wallet", "pay_wallet_transaction", "member_address"]:
        hit = collisions.get(key)
        if not hit:
            continue
        for old_id in hit:
            new_id = gen_id()
            cur.execute(f"UPDATE `{SHADOW_TABLE[key]}` SET id=%s WHERE id=%s", (new_id, old_id))
            if key == "member_user":
                cur.execute("UPDATE shadow_pay_wallet SET user_id=%s WHERE user_id=%s", (new_id, old_id))
                cur.execute("UPDATE shadow_member_address SET user_id=%s WHERE user_id=%s", (new_id, old_id))
            elif key == "pay_wallet":
                cur.execute("UPDATE shadow_pay_wallet_transaction SET wallet_id=%s WHERE wallet_id=%s", (new_id, old_id))
    dev_conn.commit()
    print(f"  ✅ [collision] 已自动重分配 {total} 个冲突 ID（级联引用已更新）")
    return True


def to_fen(v):
    """老库元(可带小数) → dev 分，round 防浮点误差"""
    return int(round((v or 0) * 100))


def _norm_mobile(v):
    """归一化手机号：去 float 尾巴/科学计数，非纯数字返回 ''"""
    if v is None:
        return ""
    s = str(v).strip()
    if "e" in s.lower():                 # 科学计数法（先于 '.' 处理）
        try:
            n = float(s)
            return str(int(n)) if n == int(n) else ""
        except ValueError:
            return ""
    if "." in s:
        head = s.split(".")[0]
        if head.isdigit():
            s = head
        else:
            return ""
    return s if s.isdigit() else ""


def to_int(v, default=None):
    """安全转 int：''/None/非数字 → default"""
    if v is None:
        return default
    s = str(v).strip()
    if not s:
        return default
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return default


def to_dec(v, default=None):
    """安全转 float：''/None/非数字 → default"""
    if v is None:
        return default
    s = str(v).strip()
    if not s:
        return default
    try:
        return float(s)
    except (ValueError, TypeError):
        return default


def db(conn_kw):
    return connect(cursorclass=DictCursor, connect_timeout=10, charset="utf8mb4", **conn_kw)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def save_phase(state, key, st):
    """原地累积 state 再落盘，避免各阶段相互覆盖断点"""
    state[key] = st
    save_state(state)


def check_complete(conn, table, rows_done):
    """重跑前完整性校验：影子表实际行数 >= 已迁移行数，否则中止"""
    if rows_done <= 0:
        return
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE[table]}`")
    actual = cur.fetchone()["c"]
    if actual < rows_done:
        raise SystemExit(
            f"[完整校验失败] {SHADOW_TABLE[table]} 实际{actual} < 已迁移{rows_done}，请 --reset 重跑")


# ============================================================
# 目标依赖
# ============================================================
def load_target_users():
    """返回 {mobile: user_id}"""
    if DEP_SOURCE == "xlsx":
        import pandas as pd
        df = pd.read_excel(XLSX_FILE, sheet_name=XLSX_SHEET_USER)
        out = {}
        for _, r in df.iterrows():
            mob = _norm_mobile(r.get("mobile"))
            if not mob:
                continue                 # 跳过 NaN/空/非数字
            out[mob] = int(r["id"])
        return out
    conn = db(DEV_DB)
    cur = conn.cursor()
    cur.execute("SELECT mobile, id FROM member_user WHERE deleted=0")
    rows = cur.fetchall()
    conn.close()
    return {str(r["mobile"]): int(r["id"]) for r in rows if r["mobile"]}


def load_target_wallets():
    """返回 {user_id: {wallet_id, balance}}"""
    if DEP_SOURCE == "xlsx":
        import pandas as pd
        df = pd.read_excel(XLSX_FILE, sheet_name=XLSX_SHEET_WALLET)
        return {int(r["user_id"]): {"wallet_id": int(r["id"]), "balance": int(r["balance"] or 0)}
                for _, r in df.iterrows()}
    conn = db(DEV_DB)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, balance FROM pay_wallet WHERE deleted=0")
    rows = cur.fetchall()
    conn.close()
    return {int(r["user_id"]): {"wallet_id": int(r["id"]), "balance": int(r["balance"] or 0)}
            for r in rows}


def rebuild_by_account(old_conn, dev_conn, target_users=None):
    """重建 by_account：影子用户（新增）+ 已存在用户（老库手机号∩线上 target，is_existing=True）
    供钱包/地址阶段使用；已存在用户走 继承线上钱包id + 余额累加"""
    dc = dev_conn.cursor()
    dc.execute("SELECT id, mobile FROM shadow_member_user WHERE mobile IS NOT NULL AND mobile<>''")
    mob_to_uid = {str(r["mobile"]): int(r["id"]) for r in dc.fetchall()}
    oc = old_conn.cursor()
    by_account = {}
    mobs = list(mob_to_uid.keys())
    for i in range(0, len(mobs), BATCH):
        chunk = mobs[i:i + BATCH]
        fmt = ",".join(["%s"] * len(chunk))
        oc.execute(
            f"SELECT u.account_id, u.phone FROM sys_user u "
            f"JOIN (SELECT MAX(id) mid FROM sys_user WHERE phone IN ({fmt}) GROUP BY phone) t ON u.id=t.mid",
            chunk)
        for r in oc.fetchall():
            uid = mob_to_uid.get(str(r["phone"]))
            if uid and r["account_id"]:
                by_account[str(r["account_id"])] = {"uid": uid, "is_existing": False}
    # 已存在用户：老库手机号在线上 target 里 → is_existing=True（继承线上钱包id+余额累加）
    if target_users:
        online = {str(m): int(u) for m, u in target_users.items()}
        op = list(online.keys())
        for i in range(0, len(op), BATCH):
            chunk = op[i:i + BATCH]
            fmt = ",".join(["%s"] * len(chunk))
            oc.execute(
                f"SELECT u.account_id, u.phone FROM sys_user u "
                f"WHERE u.role_id=5 AND u.phone IN ({fmt})", chunk)
            for r in oc.fetchall():
                uid = online.get(str(r["phone"]))
                if uid and r["account_id"] and str(r["account_id"]) not in by_account:
                    by_account[str(r["account_id"])] = {"uid": uid, "is_existing": True}
    return by_account


# ============================================================
# 建影子表
# ============================================================
def create_shadow_tables(conn):
    cur = conn.cursor()
    for key, target in [("member_user", "member_user"), ("pay_wallet", "pay_wallet"),
                        ("pay_wallet_transaction", "pay_wallet_transaction"),
                        ("member_address", "member_address")]:
        shadow = SHADOW_TABLE[key]
        cur.execute("SHOW TABLES LIKE %s", (shadow,))
        if cur.fetchone():
            print(f"  影子表已存在: {shadow}")
            continue
        cur.execute(f"CREATE TABLE `{shadow}` LIKE `{target}`")   # 先按 dev 结构建
        # 影子表字段对齐线上表：DROP 线上没有的列（member_user 19 列、pay_wallet 1 列）
        drop_cols = _DROP_COLS.get(key, [])
        for col in drop_cols:
            cur.execute(f"ALTER TABLE `{shadow}` DROP COLUMN `{col}`")
        if key == "member_user":
            # 临时中转列：存老 pay_station_id(UUID)，后置按 UUID 回填 operation_center_id，同步线上时排除
            cur.execute(
                f"ALTER TABLE `{shadow}` ADD COLUMN operation_center_uuid varchar(64) NULL DEFAULT NULL")
        print(f"  ✅ 创建影子表 {shadow} (对齐线上，{'DROP %d 列' % len(drop_cols) if drop_cols else '结构同 dev'})")
    conn.commit()


# ============================================================
# 字段映射（有老源→填；无源→None 留空）
# ============================================================
def _map_sex(v):
    """对齐 dev：0=未知、1=男、2=女"""
    s = str(v or "").lower().strip()
    if not s:
        return 0
    if s in ("male", "1", "男"):
        return 1
    if s in ("female", "2", "女"):
        return 2
    n = to_int(v)
    return n if n is not None else 0


_OLD_DEFAULT_AVATAR = "https://kejian-xianzhi.oss-cn-zhangjiakou.aliyuncs.com/admin/hys/avatar.png"
_NEW_DEFAULT_AVATAR = "https://hy-recycle-mini.oss-cn-hangzhou.aliyuncs.com/static/img/shop/default_avatar.webp"


def _map_avatar(v):
    """头像：老默认头像→新默认；空/None→NULL；其他原样（开发确认）"""
    if not v:
        return None
    s = str(v).strip()
    if not s:
        return None
    if s == _OLD_DEFAULT_AVATAR:
        return _NEW_DEFAULT_AVATAR
    return s


def map_member_user(o, new_uid, now):
    status = 0 if to_int(o.get("status")) == 1 else 1   # 老 1→dev 0，老 {2,-1}/空→dev 1
    m = {
        "id": new_uid,
        "mobile": o.get("phone"),
        "password": "",                                        # 不插老密码，留空
        "status": status,
        "nickname": o.get("nick_name") or "",
        "avatar": _map_avatar(o.get("avatar")),           # 旧默认→新默认；空/None→NULL（开发确认）
        "name": o.get("real_auth_name"),                  # 真实姓名，无实名留空
        "sex": _map_sex(o.get("sex")),
        "is_promoter": 0,                                 # 留空(按类型取0)
        "station_id": to_int(o.get("station_id")),
        "company_id": to_int(o.get("company_id")),
        "channel": o.get("channel"),
        "promotion_site_id": to_int(o.get("promotion_station_id")),
        "promotion_activity_id": to_int(o.get("promotion_activity_id")),
        "promotion_platform": None,               # 先留空（开发确认）
        "promotion_channel": None,                # 先留空（开发确认）
        "creator": "migrate",
        "create_time": o.get("created_at") or now,        # 老表创建时间
        "updater": "migrate",
        "update_time": now,                               # 当前时间
        "deleted": b"\x00",
        "tenant_id": TENANT_ID,
        # 临时中转列：老 pay_station_id(UUID)；operation_center_id 保持 NULL，后置按 UUID 回填
        "operation_center_uuid": o.get("pay_station_id"),
    }
    # 未映射列按 dev 约定填充（NOT NULL→默认值/占位，可空→NULL）
    fill_unmapped("member_user", m)
    return m


def map_pay_wallet(o, wallet_id, user_id, balance, now):
    m = {
        "id": wallet_id,
        "user_id": user_id,
        "user_type": 1,                                    # 已迁移用户为 C 端
        "balance": balance,
        "creator": "migrate",
        "create_time": o.get("created_at") or now,
        "updater": "migrate",
        "update_time": now,
        "deleted": b"\x00",
        "tenant_id": TENANT_ID,
    }
    fill_unmapped("pay_wallet", m)
    return m


def map_transaction(tx_id, wallet_id, price, balance, now):
    """按钱包余额生成一条 increase 流水（迁移收入）"""
    m = {
        "id": tx_id,
        "wallet_id": wallet_id,
        "biz_type": 0,                          # 系统导入（迁移收入，固定 0）
        "biz_id": "",
        "no": str(gen_id()),                    # 唯一流水号（雪花生成）
        "title": "系统导入",
        "price": price,                          # 正数，收入=老库钱包余额
        "balance": balance,                      # 交易后余额=dev现有+老库余额
        "creator": "migrate",
        "create_time": now,
        "updater": "migrate",
        "update_time": now,
        "deleted": b"\x00",
        "tenant_id": TENANT_ID,
    }
    fill_unmapped("pay_wallet_transaction", m)
    return m


# dev member_address 字符串列长度上限（超长截断，防 Data too long）
_ADDR_STR_MAX = {
    "name": 10, "mobile": 20,
    "province_code": 32, "province": 64,
    "city_code": 32, "city": 64,
    "district_code": 32, "district": 64,
    "detail_address": 250,
    "door_plate": 100, "community_name": 64, "community_code": 32,
}


def _fill_str(v, max_len, not_null=False):
    """string 缺失：NOT NULL 列→''（空串），可空列→NULL；非空→截断到 max_len"""
    if v is None:
        return "" if not_null else None
    s = str(v).strip()
    if not s:
        return "" if not_null else None
    return s[:max_len]


_POLLUTED_RX = re.compile(
    r"union\s+select|select\s+from|sleep\s*\(|benchmark\s*\(|md5\s*\(|"
    r"updatexml\s*\(|extractvalue\s*\(|\$\{jndi:|%bf|limit\s+\d+\s*#|0x[0-9a-fA-F]{6,}",
    re.IGNORECASE)


def _is_polluted(row):
    """检测地址行是否含注入/攻击特征（命中则整行跳过，不插入影子表）"""
    for v in row.values():
        if isinstance(v, str) and _POLLUTED_RX.search(v):
            return True
    return False


def map_address(o, addr_id, user_id, now):
    m = {
        "id": addr_id,
        "user_id": user_id,
        "name": _fill_str(o.get("name"), _ADDR_STR_MAX["name"], True),          # NOT NULL→空串
        "mobile": _fill_str(o.get("phone"), _ADDR_STR_MAX["mobile"], True),     # NOT NULL→空串
        "area_id": to_int(o.get("district_code"), 0),    # int NOT NULL，缺失→0（schema强制）
        "province_code": _fill_str(o.get("province_code"), _ADDR_STR_MAX["province_code"]),
        "province": _fill_str(o.get("province"), _ADDR_STR_MAX["province"]),
        "city_code": _fill_str(o.get("city_code"), _ADDR_STR_MAX["city_code"]),
        "city": _fill_str(o.get("city"), _ADDR_STR_MAX["city"]),
        "district_code": _fill_str(o.get("district_code"), _ADDR_STR_MAX["district_code"]),
        "district": _fill_str(o.get("district"), _ADDR_STR_MAX["district"]),
        "detail_address": _fill_str(o.get("address_detail"), _ADDR_STR_MAX["detail_address"], True),  # NOT NULL→空串
        "default_status": b"\x01" if o.get("default") else b"\x00",
        "creator": "migrate",
        "create_time": o.get("created_at") or now,
        "updater": "migrate",
        "update_time": o.get("updated_at") or now,
        "deleted": b"\x00",
        "tenant_id": TENANT_ID,
        "door_plate": _fill_str(o.get("house_no"), _ADDR_STR_MAX["door_plate"]),
        "community_name": _fill_str(o.get("community_name"), _ADDR_STR_MAX["community_name"]),
        "community_code": _fill_str(o.get("community_code"), _ADDR_STR_MAX["community_code"]),
        "longitude": to_dec(o.get("longitude")),      # decimal 缺失→NULL
        "latitude": to_dec(o.get("latitude")),        # decimal 缺失→NULL
    }
    fill_unmapped("member_address", m)
    return m


_table_cols_cache = {}


def insert_batch(conn, table, rows):
    if not rows:
        return
    # 只插影子表实际存在的列（map 返回的 dev 全字段中，多余 key 自动剔除）
    if table not in _table_cols_cache:
        cur = conn.cursor()
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        _table_cols_cache[table] = {r["Field"] for r in cur.fetchall()}
    cols = _table_cols_cache[table]
    keys = [k for k in rows[0].keys() if k in cols]
    if not keys:
        return
    ck = ", ".join(f"`{k}`" for k in keys)
    ph = ", ".join(["%s"] * len(keys))
    sql = f"INSERT INTO `{table}` ({ck}) VALUES ({ph})"
    conn.cursor().executemany(sql, [tuple(r[k] for k in keys) for r in rows])
    conn.commit()


# ============================================================
# 1. 用户迁移（全局手机号去重取最新）
#    返回 {account_id(UUID): {uid, is_existing}}，供钱包/地址关联
# ============================================================
def migrate_member_user(old_conn, dev_conn, target_users, state, limit=0):
    key = "member_user"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  member_user 已迁移完成，跳过（重建 by_account 供后续阶段）")
        return rebuild_by_account(old_conn, dev_conn, target_users)
    check_complete(dev_conn, key, st["rows"])

    cur = old_conn.cursor()
    sql = (
        "SELECT u.id, u.phone, u.account_id FROM sys_user u "
        "JOIN (SELECT MAX(id) mid FROM sys_user "
        f"WHERE role_id=5 AND phone IS NOT NULL AND phone<>'' AND phone REGEXP '{PHONE_RE}' "
        "GROUP BY phone) t ON u.id=t.mid")
    args = None
    if limit:
        sql += " ORDER BY u.id DESC LIMIT %s"      # 试运行：取最新 N 个用户
        args = (limit,)
    cur.execute(sql, args)
    candidates = cur.fetchall()
    print(f"  [member_user] 待处理候选用户(去重+手机号过滤后): {len(candidates)}")

    target_mobiles = set(target_users.keys())
    by_account = {}        # account_id → {"uid": 最终user_id, "is_existing": bool}
    to_migrate = []        # (id, phone, account_id) 需要 INSERT 的新用户
    for c in candidates:
        pid = int(c["id"])
        phone = str(c["phone"])
        acc = str(c["account_id"] or "")
        if not acc:
            continue
        if phone in target_mobiles:
            by_account[acc] = {"uid": int(target_users[phone]), "is_existing": True}
        else:
            to_migrate.append((pid, phone, acc))
    to_migrate.sort()
    print(f"  [member_user] 新用户待迁: {len(to_migrate)}, 已存在(累加钱包): {len(by_account)}")

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    rows_done = st["rows"]
    ids = [x[0] for x in to_migrate]
    done_ids = st["last_id"]
    start_idx = next((i for i, x in enumerate(ids) if x > done_ids), len(ids)) if done_ids else 0
    for i in range(start_idx, len(ids), BATCH):
        chunk_ids = ids[i:i + BATCH]
        fmt = ",".join(["%s"] * len(chunk_ids))
        cur.execute(f"SELECT * FROM sys_user WHERE id IN ({fmt})", chunk_ids)
        rows = cur.fetchall()
        mapped = [map_member_user(r, gen_id(), now) for r in rows]
        insert_batch(dev_conn, SHADOW_TABLE[key], mapped)
        for j, r in enumerate(rows):
            by_account[str(r["account_id"])] = {"uid": mapped[j]["id"], "is_existing": False}
        rows_done += len(mapped)
        st["last_id"] = chunk_ids[-1]
        st["rows"] = rows_done
        save_phase(state, key, st)
        print(f"  [member_user] {i//BATCH+1}批: +{len(mapped)} (累计{rows_done})")
    if not limit:                          # 试运行不标记完成，避免影响后续全量
        st["done"] = True
    save_phase(state, key, st)
    print(f"  ✅ member_user 迁移完成，共 {rows_done} 行")
    return by_account


# ============================================================
# 2. 钱包迁移（owner_id 为 account_id UUID；增量断点；余额×100）
#    返回 {老wallet.wallet_id(UUID): {"wallet_id": 新id, "user_id": uid}}，供流水关联
#    （wallet_log.wallet_id 引用的是 wallet.wallet_id，非 wallet.id）
# ============================================================
def migrate_pay_wallet(old_conn, dev_conn, by_account, target_wallets, state, limit=0):
    key = "pay_wallet"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  pay_wallet 已迁移完成，跳过")
        return {}
    check_complete(dev_conn, key, st["rows"])

    cur = old_conn.cursor()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    wallet_map = {}

    def build(rows):
        to_insert = []
        for r in rows:
            info = by_account.get(str(r["owner_id"] or ""))
            if not info:
                continue
            price = to_fen(r["balance"])                      # 收入=老库余额（可为负）
            if info["is_existing"]:
                tw = target_wallets.get(info["uid"])
                if tw:
                    wallet_id = tw["wallet_id"]
                    balance = tw["balance"] + to_fen(r["balance"])   # 累加(分)，保留负
                else:
                    wallet_id = gen_id()                              # 无目标钱包→新建
                    balance = to_fen(r["balance"])
            else:
                wallet_id = gen_id()
                balance = to_fen(r["balance"])
            wallet_map[str(r["wallet_id"])] = {
                "wallet_id": wallet_id,
                "user_id": info["uid"],
                "price": price,                  # 迁移收入=老库余额（可为负）
                "balance": balance,              # 最终影子余额（dev现有+老库，保留负）
            }
            to_insert.append(map_pay_wallet(r, wallet_id, info["uid"], balance, now))
        return to_insert

    if limit:                            # 试运行：只处理这批用户的钱包
        acc_ids = list(by_account.keys())
        fmt = ",".join(["%s"] * len(acc_ids))
        cur.execute(
            "SELECT id, wallet_id, owner_id, wallet_type, balance, created_at, updated_at "
            f"FROM wallet WHERE owner_id IN ({fmt})", acc_ids)
        to_insert = build(cur.fetchall())
        for i in range(0, len(to_insert), BATCH):
            insert_batch(dev_conn, SHADOW_TABLE[key], to_insert[i:i + BATCH])
        st["rows"] = len(to_insert)
        save_phase(state, key, st)
        print(f"  ✅ [pay_wallet 试运行] 共 {len(to_insert)} 行")
        return wallet_map

    cur.execute("SELECT COUNT(*) c FROM wallet")
    total = cur.fetchone()["c"]
    print(f"  [pay_wallet] 老钱包总数: {total}")
    rows_done = st["rows"]
    last = st["last_id"]
    batch_no = 0
    while True:
        cur.execute(
            "SELECT id, wallet_id, owner_id, wallet_type, balance, created_at, updated_at "
            "FROM wallet WHERE id > %s ORDER BY id LIMIT %s", (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        to_insert = build(rows)
        insert_batch(dev_conn, SHADOW_TABLE[key], to_insert)
        rows_done += len(to_insert)
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        save_phase(state, key, st)
        batch_no += 1
        if batch_no % 10 == 0:
            print(f"  [pay_wallet] 第{batch_no}批: 累计{rows_done}/{total}")
    st["done"] = True
    save_phase(state, key, st)
    print(f"  ✅ pay_wallet 迁移完成，共 {rows_done} 行")
    return wallet_map


# ============================================================
# 3. 流水生成（不再读老库 wallet_log；按钱包老库余额>0 各生成一条 increase）
# ============================================================
def migrate_transaction(dev_conn, wallet_map, state):
    key = "pay_wallet_transaction"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  pay_wallet_transaction 已生成完成，跳过")
        return
    check_complete(dev_conn, key, st["rows"])

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    to_insert = []
    for w in wallet_map.values():
        if w["price"] == 0:                     # 0金额不生成流水；负数生成（负数金额）
            continue
        to_insert.append(map_transaction(gen_id(), w["wallet_id"], w["price"], w["balance"], now))
    for i in range(0, len(to_insert), BATCH):
        insert_batch(dev_conn, SHADOW_TABLE[key], to_insert[i:i + BATCH])
    st["rows"] = len(to_insert)
    st["done"] = True
    save_phase(state, key, st)
    print(f"  ✅ pay_wallet_transaction 生成完成，共 {len(to_insert)} 行")


# ============================================================
# 4. 地址迁移（新ID，user_id 继承；account_id 为 UUID）
# ============================================================
def migrate_member_address(old_conn, dev_conn, by_account, state, limit=0):
    key = "member_address"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  member_address 已迁移完成，跳过")
        return
    check_complete(dev_conn, key, st["rows"])

    cur = old_conn.cursor()
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    if limit:                            # 试运行：只处理这批用户的地址
        acc_ids = list(by_account.keys())
        fmt = ",".join(["%s"] * len(acc_ids))
        cur.execute(f"SELECT * FROM user_address WHERE account_id IN ({fmt})", acc_ids)
        mapped = []
        for r in cur.fetchall():
            if _is_polluted(r):              # 污染数据（注入/攻击特征）不插入
                continue
            info = by_account.get(str(r["account_id"] or ""))
            if not info:
                continue
            mapped.append(map_address(r, gen_id(), info["uid"], now))
        for i in range(0, len(mapped), BATCH):
            insert_batch(dev_conn, SHADOW_TABLE[key], mapped[i:i + BATCH])
        st["rows"] = len(mapped)
        save_phase(state, key, st)
        print(f"  ✅ [address 试运行] 共 {len(mapped)} 行")
        return

    rows_done = st["rows"]
    last = st["last_id"]
    batch_no = 0
    while True:
        cur.execute(
            "SELECT * FROM user_address WHERE id > %s ORDER BY id LIMIT %s", (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        to_insert = []
        for r in rows:
            if _is_polluted(r):              # 污染数据（注入/攻击特征）不插入
                continue
            info = by_account.get(str(r["account_id"] or ""))
            if not info:
                continue
            to_insert.append(map_address(r, gen_id(), info["uid"], now))
        insert_batch(dev_conn, SHADOW_TABLE[key], to_insert)
        rows_done += len(to_insert)
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        save_phase(state, key, st)
        batch_no += 1
        if batch_no % 5 == 0:
            print(f"  [address] 第{batch_no}批: 累计{rows_done}")
    st["done"] = True
    save_phase(state, key, st)
    print(f"  ✅ member_address 迁移完成，共 {rows_done} 行")


# ============================================================
# main
# ============================================================
def main():
    args = sys.argv[1:]
    old_conn = db(OLD_DB)
    dev_conn = db(DEV_DB)
    state = load_state()

    if "--init" in args:
        create_shadow_tables(dev_conn)
        print("影子表创建完成（未执行迁移）")
        return
    if "--reset" in args:
        for t in SHADOW_TABLE.values():
            dev_conn.cursor().execute(f"DROP TABLE IF EXISTS `{t}`")
        dev_conn.commit()
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("已清空影子表与状态")
        return

    create_shadow_tables(dev_conn)

    if "--check" in args:
        cur = dev_conn.cursor()
        for key, table in SHADOW_TABLE.items():
            cur.execute(f"SELECT COUNT(*) c FROM `{table}`")
            print(f"  {table}: {cur.fetchone()['c']} 行")
        return

    preload_used_ids(dev_conn)
    print(f"已预加载 {len(_used_ids)} 个现有 ID，避免生成冲突")

    if "--collide-check" in args:
        check_id_collision(dev_conn, auto_fix=True)
        return

    limit = 0
    if "--limit" in args:
        try:
            limit = int(args[args.index("--limit") + 1])
        except (IndexError, ValueError):
            raise SystemExit("--limit 需要数字参数，如 --limit 5000")
        print(f"试运行模式：仅迁移最新 {limit} 个用户")

    target_users = load_target_users()
    target_wallets = load_target_wallets()
    print(f"目标依赖({DEP_SOURCE}): 已有用户 {len(target_users)}, 已有钱包 {len(target_wallets)}")

    by_account = migrate_member_user(old_conn, dev_conn, target_users, state, limit)
    by_account = rebuild_by_account(old_conn, dev_conn, target_users)   # 无条件重建，保证钱包/地址 by_account 完整
    print(f"  [by_account] 已重建 {len(by_account)} 条（钱包/地址阶段使用）")
    wallet_map = migrate_pay_wallet(old_conn, dev_conn, by_account, target_wallets, state, limit)
    migrate_transaction(dev_conn, wallet_map, state)
    migrate_member_address(old_conn, dev_conn, by_account, state, limit)

    print("\n===== 迁移结果自检 =====")
    cur = dev_conn.cursor()
    for key, table in SHADOW_TABLE.items():
        cur.execute(f"SELECT COUNT(*) c FROM `{table}`")
        print(f"  {table}: {cur.fetchone()['c']} 行")
    cur.execute("SELECT COUNT(*) c FROM shadow_pay_wallet WHERE balance > 0")
    print(f"  有余额钱包: {cur.fetchone()['c']}")
    cur.execute("SELECT COUNT(*) c FROM shadow_pay_wallet_transaction")
    print(f"  流水总数: {cur.fetchone()['c']}")
    cur.execute("SELECT COUNT(*) c FROM shadow_member_user WHERE operation_center_uuid IS NOT NULL")
    print(f"  有 operation_center_uuid 用户: {cur.fetchone()['c']}")
    check_id_collision(dev_conn, auto_fix=True)
    print("（可用 --check 复查；自检通过后如要全量，先 --reset 清空试跑数据）")


if __name__ == "__main__":
    main()
