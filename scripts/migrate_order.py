#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单迁移脚本：老 order → shadow_recycle_order，同时处理订单明细 老 order_product → shadow_recycle_order_item。

订单过滤（开发确认，保证数据干净）：
  - order.package_code 为空（NULL/''）→ 整单不迁
  - package_code 按分隔符 [,，、;；\s]+ 切出的值数 ≠ 该订单 order_product 行数 → 整单不迁
    （值数必须等于明细数，多或少都不迁）
  - 本地库实测：可迁 346,510（81.8%），过滤 77,065（18.2% = 空码17.9% + 不匹配0.4%）

明细合并（单脚本同时处理，位置配对）：
  - 明细按 op.id 升序与 package_code 切值位置一一对应：第 i 明细 ↔ 第 i 个包裹码
  - item_code = 订单 package_code 位置码（不查 op.package_code / express_order / order_no）
  - item 其余字段当场填全（item_pic/price/weight/total_price/create_time/update_time 来自 order_product）
  - item_id=固定 2047530778823024642、item_name=固定 '统货'、item_unit=固定 'KG'

订单映射规则（开发已确认，2026-08）：
  - order_no      : snowflake 自生成（uk_order_no 唯一），不映射老 order_id
  - user_id       : account_id → 新 member_user.id（复用 rebuild_by_account，含线上已存在用户）
  - total_price / pay_price : 都写老 pay_money（元，保留2位小数）
  - status/sub_status/cancel_type/settlement_status/inspect_status : 完全按官方映射表
    /Users/rs/Documents/order-recycle_order.xlsx（_STATUS_MAP 表驱动）：
      老1→10/11、老3→10/21、老4→10/22、老5→20/23、
      老6·10~60→30/32+结算30+质检20、老999→30/32、
      老-1→50/51+取消0、老-2→50/52+取消1、
      老-10→50/55+取消2、老-3/2/-20→status/sub_status 置 NULL，其余列 NULL
  - order_type    : biz_mode WeightClothes→0(在线) SiteStationWeight→1(面对面) ExclusiveWeightClothes→2(专属) 其他→0
  - settlement_type : operation_center_settle_type ExpressWeight→1(回收结算) FactoryQa→2(到场结算) ActivityRewardDonate→1
  - real_weight   : express_real_weight（decimal(10,3)）
  - pre_weight    : predict_weight（varchar）
  - weight_time   : service_station_recycle_completed_time（复用回收完成时间）
  - lat/lon       : 老 lat=纬度、lon=经度（实测），直接 lat→lat、lon→lon
  - promotion_platform / promotion_channel / appointment_photos 等 : null（开发确认）
  - pay_type=2（钱包余额）；pay_time=recycle_end_time（=service_station_recycle_completed_time，1970→NULL）
  - 按 biz_mode 分支（2026-08 新版本）：
    线上 WeightClothes：express_net_code=service_station_id、express_emp_code=service_station_receive_order_account_id、
      express_emp_phone=service_station_receive_tp_phone、recycler_user_id/phone=receive_order_account_id/tp_phone、real_weight=express_real_weight
    线下 SiteStationWeight：real_weight=pay_kg、total_price/pay_price=pay_money、recycler_user_id/phone=NULL、express_* 三字段=NULL
  - 线下订单（SiteStationWeight）在 package 迁移后经 --offline 模式补迁（不涉及 recycle_package_item）
  - operation_center_id : null（后置按 UUID 回填）；老 operation_center_id(UUID) 存临时列 operation_center_uuid
  - 软删(deleted_at NOT NULL) 不迁移
  - 污染数据（_is_polluted）整行跳过

幂等：启动载入 shadow_recycle_order.order_id_old 集合，重复订单（含其明细）整单跳过。

用法：
    python scripts/migrate_order.py --init       # 只建影子表（订单+明细）
    python scripts/migrate_order.py --reset      # 清空影子表+状态
    python scripts/migrate_order.py --limit N    # 试运行：只处理已迁移用户(by_account)的订单
    python scripts/migrate_order.py              # 全量（断点续传）：线上过滤订单
    python scripts/migrate_order.py --offline    # 线下：面对面(SiteStationWeight)订单，package 迁移后执行
    python scripts/migrate_order.py --check      # 查看影子表行数
"""
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pymysql.cursors import DictCursor  # noqa: E402

from migrate_old_db_to_shadow import (  # noqa: E402
    db, DEV_DB, OLD_DB, BATCH, gen_id, insert_batch, rebuild_by_account,
    load_target_users, load_prod_collision, to_int, to_dec, preload_used_ids,
    _used_ids, _is_polluted,
)

SHADOW_ORDER = "shadow_recycle_order"
SHADOW_ITEM = "shadow_recycle_order_item"
STATE_FILE = PROJECT_ROOT / "scripts" / ".migrate_order_state.json"

# 面对面（线下）订单迁移开关：默认关；设置环境变量 MIGRATE_OFFLINE=1 开启
OFFLINE_ENABLED = os.getenv("MIGRATE_OFFLINE", "0") == "1"

ITEM_ID_FIXED = 2047530778823024642   # 固定回收物id（ERP 统货产品）
ITEM_NAME_FIXED = "统货"
ITEM_UNIT_FIXED = "KG"

ORDER_TYPE_MAP = {
    "WeightClothes": 0,           # 在线
    "SiteStationWeight": 1,       # 面对面
    "ExclusiveWeightClothes": 2,  # 专属
}
SETTLE_TYPE_MAP = {
    "ExpressWeight": 1,           # 回收结算
    "FactoryQa": 2,               # 到场结算
    "ActivityRewardDonate": 1,
}
# 官方映射表（/Users/rs/Documents/order-recycle_order.xlsx，开发确认）
# 每项 = (status, sub_status, cancel_type, settlement_status, inspect_status)
_STATUS_MAP = {
    1: (10, 11, None, None, None),
    3: (10, 21, None, None, None),
    4: (10, 22, None, None, None),
    5: (20, 23, None, None, None),
    6: (30, 32, None, None, None),
    999: (30, 32, None, None, None),
    -1: (50, 51, 0, None, None),
    -2: (50, 52, 1, None, None),
    -10: (50, 55, 2, None, None),
    -3: (None, None, None, None, None),   # 未覆盖状态 → 置 NULL（开发确认）
    2: (None, None, None, None, None),
    -20: (None, None, None, None, None),
}
for _s in (6, 10, 11, 12, 13, 20, 21, 22, 23, 30, 31, 32, 33, 34, 35,
           40, 41, 42, 43, 44, 50, 60):
    _STATUS_MAP[_s] = (30, 32, None, 30, 20)
_STR_MAX = {
    "user_name": 64, "province_code": 32, "province": 64, "city_code": 32,
    "city": 64, "district_code": 32, "district": 64, "address_detail": 255,
    "door_plate": 100, "community_name": 64, "community_code": 32,
}
_order_nos = set()
_PKG_SPLIT_RX = re.compile(r"[,，、;；\s]+")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def preload_order_nos(dev_conn):
    """预加载 dev recycle_order 既有 order_no + prod 碰撞表 order_no，避免雪花订单号冲突（uk_order_no）"""
    cur = dev_conn.cursor()
    cur.execute("SELECT order_no FROM recycle_order")
    for r in cur.fetchall():
        _order_nos.add(str(r["order_no"]))
    _order_nos |= load_prod_collision()["order_nos"]


def preload_recycle_ids(dev_conn):
    """把 dev 真实表 recycle_order/recycle_order_item 的 id 并入 _used_ids，防雪花冲突"""
    cur = dev_conn.cursor()
    for t in ("recycle_order", "recycle_order_item"):
        try:
            cur.execute(f"SELECT id FROM `{t}`")
            for r in cur.fetchall():
                _used_ids.add(int(r["id"]))
        except Exception:
            pass


def gen_order_no():
    while True:
        n = str(gen_id())
        if n not in _order_nos:
            _order_nos.add(n)
            return n


def _trunc(v, max_len):
    if v is None:
        return None
    s = str(v).strip()
    return s[:max_len]


def _money(v, nd=2):
    """decimal 字段：float → round 到 nd 位，None 透传"""
    x = to_dec(v)
    return round(x, nd) if x is not None else None


def _pre_w(v):
    """pre_weight（varchar）：float → 去尾零字符串"""
    x = to_dec(v)
    return None if x is None else f"{x:g}"


def _fix_1970(v):
    """老系统未真正入写的占位时间(1970-01-01) → NULL（开发确认，避免线上显示1970）"""
    if v is None:
        return None
    if isinstance(v, datetime) and v.year <= 1970:
        return None
    return v


def _split_package_codes(code):
    """package_code 按分隔符切值，返回非空值列表"""
    if not code:
        return []
    return [x for x in _PKG_SPLIT_RX.split(str(code)) if x]


_TEMP_COLS = [
    "operation_center_uuid",   # 老 order.operation_center_id(UUID)，后置回填 operation_center_id
    "order_id_old",            # 老 order.order_id(UUID)，幂等去重/明细关联
]


def _ensure_temp_col(conn):
    """确保临时列存在（幂等；同步线上时排除）"""
    cur = conn.cursor()
    for col in _TEMP_COLS:
        cur.execute(f"SHOW COLUMNS FROM `{SHADOW_ORDER}` LIKE '{col}'")
        if not cur.fetchone():
            cur.execute(
                f"ALTER TABLE `{SHADOW_ORDER}` ADD COLUMN {col} varchar(64) NULL DEFAULT NULL")
            conn.commit()


def create_shadow_tables(conn):
    cur = conn.cursor()
    for table, src in ((SHADOW_ORDER, "recycle_order"), (SHADOW_ITEM, "recycle_order_item")):
        cur.execute("SHOW TABLES LIKE %s", (table,))
        if cur.fetchone():
            print(f"  影子表已存在: {table}")
        else:
            cur.execute(f"CREATE TABLE `{table}` LIKE `{src}`")
            print(f"  ✅ 创建影子表 {table} (like {src})")
    _ensure_temp_col(conn)
    conn.commit()


def check_complete(conn, table, rows_done):
    """重跑前完整性校验：影子表实际行数 >= 已迁移行数，否则中止"""
    if rows_done <= 0:
        return
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) c FROM `{table}`")
    actual = cur.fetchone()["c"]
    if actual < rows_done:
        raise SystemExit(
            f"[完整校验失败] {table} 实际{actual} < 已迁移{rows_done}，请 --reset 重跑")


def map_order(o, order_id, user_id, now):
    """老 order 行 → dev recycle_order 行（映射定稿）

    按 biz_mode 分支（开发确认，2026-08 新版本）：
      - WeightClothes（线上）：express_net_code=service_station_id、express_emp_code=receive_order_account_id、
        express_emp_phone=receive_tp_phone、recycler_user_id/phone=receive_order_account_id/tp_phone、real_weight=express_real_weight
      - SiteStationWeight（线下）：real_weight=pay_kg、recycler_user_id/phone=NULL、express_* 三字段=NULL
    """
    biz = o.get("biz_mode") or ""
    is_offline = (biz == "SiteStationWeight")
    settle_type = o.get("operation_center_settle_type")
    st, sub, cancel_type, settlement_status, inspect_status = _STATUS_MAP.get(
        to_int(o.get("status")), (None, None, None, None, None))
    return {
        "id": order_id,
        "order_no": gen_order_no(),
        "order_type": ORDER_TYPE_MAP.get(biz, 0),
        "platform": o.get("platform"),
        "provider": None,
        "channel": o.get("channel") or None,            # 老有值即刷，无值→NULL（开发确认）
        "scene": None,
        "promoter_id": None,                            # 不处理（开发确认置空）
        "promotion_platform": None,                     # 留空（开发确认）
        "promotion_channel": None,                      # 留空（开发确认）
        "promotion_station_id": o.get("promotion_station_id"),
        "user_id": user_id,
        "user_phone": o.get("user_phone"),
        "user_name": _trunc(o.get("user_name"), _STR_MAX["user_name"]),
        "province_code": _trunc(o.get("province_code"), _STR_MAX["province_code"]),
        "province": _trunc(o.get("province"), _STR_MAX["province"]),
        "city_code": _trunc(o.get("city_code"), _STR_MAX["city_code"]),
        "city": _trunc(o.get("city"), _STR_MAX["city"]),
        "district_code": _trunc(o.get("district_code"), _STR_MAX["district_code"]),
        "district": _trunc(o.get("district"), _STR_MAX["district"]),
        "appointment_date": o.get("appointment_date"),
        "appointment_time_period": o.get("appointment_time_period"),
        "appointment_week_str": o.get("appointment_week_str"),
        "address_detail": _trunc(o.get("address_detail"), _STR_MAX["address_detail"]),
        "appointment_photos": None,                     # 不填 pics（开发确认）
        "express_type": o.get("express_type"),
        "express_name": None,
        "express_order": o.get("express_order"),
        "express_cost": _money(o.get("express_cost")),
        "express_status": o.get("express_status"),
        "express_meterage_weight": _money(o.get("express_meterage_weight")),
        "pre_weight": _pre_w(o.get("predict_weight")),
        "real_weight": _money(o.get("pay_kg" if is_offline else "express_real_weight"), nd=3),  # 线下取pay_kg/线上取express_real_weight
        "package_num": to_int(o.get("package_num"), 0),
        "total_price": _money(o.get("pay_money")),      # 都写老 pay_money（元）
        "pay_price": _money(o.get("pay_money")),
        "pay_type": 2,                                  # 统一 2 钱包余额（开发确认）
        "settlement_type": SETTLE_TYPE_MAP.get(settle_type),
        "cancel_time": None,
        "cancel_type": cancel_type,                     # 官方表：-1→0 / -2→1 / -10→2
        "status": st,                                   # 官方表映射
        "clear_status": 0,
        "sub_status": sub,                              # 官方表映射
        "inspect_status": inspect_status,               # 官方表：10~60→20，其余 NULL
        "activity_id": to_int(o.get("activity_id")),
        "lat": to_dec(o.get("lat")),                    # 老 lat=纬度（实测）
        "lon": to_dec(o.get("lon")),                    # 老 lon=经度
        "receive_time": _fix_1970(o.get("service_station_receive_order_time")),
        "recycle_begin_time": _fix_1970(o.get("service_station_start_to_door_time")),
        "recycle_end_time": _fix_1970(o.get("service_station_recycle_completed_time")),
        "pay_time": _fix_1970(o.get("service_station_recycle_completed_time")),   # = recycle_end_time（开发确认）
        "inspect_time": _fix_1970(o.get("operation_center_finish_time")),
        "settlement_status": settlement_status,         # 官方表：10~60→30，其余 NULL
        "weight_time": _fix_1970(o.get("service_station_recycle_completed_time")),  # 复用回收完成时间
        "recycler_user_id": None if is_offline else o.get("service_station_receive_order_account_id"),  # 线下置空
        "recycler_user_name": None,
        "recycler_user_phone": None if is_offline else o.get("service_station_receive_tp_phone"),        # 线下置空
        "station_id": None,                             # 不管（开发确认）
        "warehouse_id": None,                           # 不管（开发确认）
        "operation_center_id": None,                    # 后置按 UUID 回填
        "operation_center_uuid": o.get("operation_center_id"),   # 临时列存老 UUID
        "order_id_old": o.get("order_id"),              # 临时列存老业务订单键(UUID)
        "company_id": None,
        "creator": "migrate",
        "create_time": o.get("created_at") or now,
        "updater": "migrate",
        "update_time": now,
        "deleted": b"\x00",
        "tenant_id": 1,
        "express_status_desc": None,
        "door_plate": _trunc(o.get("house_num"), _STR_MAX["door_plate"]),
        "community_name": _trunc(o.get("community_name"), _STR_MAX["community_name"]),
        "community_code": _trunc(o.get("community_code"), _STR_MAX["community_code"]),
        "address_longitude": None,
        "address_latitude": None,
        "detail_address": None,                         # 留空/不处理（开发确认）
        "express_emp_code": None if is_offline else o.get("service_station_receive_order_account_id"),  # 线下置空；线上=接单人id（开发确认）
        "express_emp_phone": None if is_offline else o.get("service_station_receive_tp_phone"),          # 线下置空；线上=接单三方电话
        "express_net_code": None if is_offline else o.get("service_station_id"),                          # 线下置空；线上=服务站id（开发确认）
        "volume": None,
        "cancel_reason": None,
        "address_id": 0,                                # NOT NULL 默认0
        "third_order_no": None,
    }


def map_item(op, item_id, order_id, package_code, now):
    """order_product 行 + 位置包裹码 → dev recycle_order_item 行"""
    price = _money(op.get("recycle_price"))
    weight = _money(op.get("num"), nd=3)
    total = round((price or 0) * (weight or 0), 2) if (price is not None and weight is not None) else None
    return {
        "id": item_id,
        "order_id": order_id,
        "item_id": ITEM_ID_FIXED,                                  # 固定
        "item_code": _trunc(package_code, 64),                     # 订单 package_code 位置码
        "item_name": ITEM_NAME_FIXED,                              # 固定
        "item_unit": ITEM_UNIT_FIXED,                              # 固定
        "item_pic": None,                                          # 统一 NULL（开发确认）
        "price": price,                                            # 元，2位
        "weight": weight,                                          # kg，3位
        "total_price": total,                                      # price×weight
        "creator": "migrate",
        "create_time": op.get("created_at") or now,
        "updater": "migrate",
        "update_time": op.get("updated_at") or now,
        "deleted": b"\x00",
        "tenant_id": 1,
    }


def load_processed_order_ids(dev_conn):
    """已迁移订单的 order_id_old 集合（幂等去重用）"""
    cur = dev_conn.cursor()
    cur.execute(f"SELECT order_id_old FROM `{SHADOW_ORDER}` WHERE order_id_old IS NOT NULL AND order_id_old<>''")
    return {str(r["order_id_old"]) for r in cur.fetchall()}


def build_batch(order_rows, by_account, prod_by_order, now):
    """处理一批订单，返回 (订单行列表, 明细行列表, 统计dict)"""
    order_ins = []
    item_ins = []
    stat = {"no_user": 0, "polluted": 0, "empty_pkg": 0, "mismatch": 0}
    for r in order_rows:
        info = by_account.get(str(r["account_id"] or ""))
        if not info:
            stat["no_user"] += 1
            continue
        if _is_polluted(r):
            stat["polluted"] += 1
            continue
        codes = _split_package_codes(r.get("package_code"))
        if not codes:
            stat["empty_pkg"] += 1
            continue
        products = prod_by_order.get(str(r["order_id"] or ""), [])
        if len(codes) != len(products):
            stat["mismatch"] += 1
            continue
        order_id = gen_id()
        order_ins.append(map_order(r, order_id, info["uid"], now))
        for code, p in zip(codes, products):
            if _is_polluted(p):
                continue
            item_ins.append(map_item(p, gen_id(), order_id, code, now))
    return order_ins, item_ins, stat


def build_batch_offline(order_rows, by_account, prod_by_order, now):
    """线下订单（面对面）：无 package_code 过滤，明细 item_code 留空（开发确认）"""
    order_ins = []
    item_ins = []
    stat = {"no_user": 0, "polluted": 0}
    for r in order_rows:
        info = by_account.get(str(r["account_id"] or ""))
        if not info:
            stat["no_user"] += 1
            continue
        if _is_polluted(r):
            stat["polluted"] += 1
            continue
        order_id = gen_id()
        order_ins.append(map_order(r, order_id, info["uid"], now))
        for p in prod_by_order.get(str(r["order_id"] or ""), []):
            if _is_polluted(p):
                continue
            item_ins.append(map_item(p, gen_id(), order_id, None, now))   # item_code 留空
    return order_ins, item_ins, stat


def migrate_order(old_conn, dev_conn, by_account, state, limit=0, offline=False):
    suffix = "_offline" if offline else ""
    key_o = "recycle_order" + suffix
    key_i = "recycle_order_item" + suffix
    st = state.get(key_o, {"last_id": 0, "rows": 0, "done": False})
    st_i = state.get(key_i, {"rows": 0, "done": False})
    if st["done"]:
        print(f"  {key_o} / {key_i} 已迁移完成，跳过")
        return
    check_complete(dev_conn, SHADOW_ORDER, st["rows"])
    check_complete(dev_conn, SHADOW_ITEM, st_i["rows"])

    cur = old_conn.cursor()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    rows_done = st["rows"]
    items_done = st_i["rows"]
    stat_tot = {"no_user": 0, "polluted": 0, "empty_pkg": 0, "mismatch": 0} if not offline else {"no_user": 0, "polluted": 0}

    # 防护（仅线上全量）：影子表已有行但无断点 → 强制先 --reset。
    # 线下模式依赖 order_id_old 幂等去重（线上订单已在影子表属正常），不做此拦截。
    if not limit and not offline and st.get("last_id", 0) == 0:
        cur_c = dev_conn.cursor()
        cur_c.execute(f"SELECT COUNT(*) c FROM `{SHADOW_ORDER}`")
        if cur_c.fetchone()["c"] > 0:
            raise SystemExit(
                f"[保护] {SHADOW_ORDER} 已有数据但无断点，可能为试运行遗留。请先 --reset 再全量")

    # 幂等：已迁移订单整单跳过（订单+明细）；线下模式即使 limit 也启用，避免重复已迁的面对面订单
    processed = load_processed_order_ids(dev_conn) if (not limit or offline) else set()
    if processed:
        print(f"  [幂等] 已迁移订单 {len(processed)} 个，跳过重复")

    # 线上轮排除面对面(SiteStationWeight)订单（面对面仅由 --offline 按开关处理）
    biz_filter = " AND biz_mode='SiteStationWeight'" if offline else " AND biz_mode<>'SiteStationWeight'"
    build = build_batch_offline if offline else build_batch

    if limit:
        # 试运行：只处理已迁移用户(by_account)的订单
        acc_ids = list(by_account.keys())
        for i in range(0, len(acc_ids), 5000):
            chunk = acc_ids[i:i + 5000]
            fmt = ",".join(["%s"] * len(chunk))
            cur.execute(
                f"SELECT * FROM `order` WHERE deleted_at IS NULL AND account_id IN ({fmt}){biz_filter}",
                chunk)
            rows = cur.fetchall()
            if processed:
                rows = [r for r in rows if str(r.get("order_id") or "") not in processed]
            oids = [str(r["order_id"]) for r in rows if r.get("order_id")]
            prod_by_order = {}
            if oids:
                pf = ",".join(["%s"] * len(oids))
                cur.execute(
                    f"SELECT * FROM order_product WHERE order_id IN ({pf}) ORDER BY order_id, id", oids)
                for p in cur.fetchall():
                    prod_by_order.setdefault(str(p["order_id"]), []).append(p)
            order_ins, item_ins, stat = build(rows, by_account, prod_by_order, now)
            insert_batch(dev_conn, SHADOW_ORDER, order_ins)
            insert_batch(dev_conn, SHADOW_ITEM, item_ins)
            rows_done += len(order_ins)
            items_done += len(item_ins)
            for k in stat_tot:
                stat_tot[k] += stat[k]
        st["rows"] = rows_done
        st_i["rows"] = items_done
        save_state(state)
        print(f"  ✅ [试运行{' 线下' if offline else ''}] 订单 {rows_done} 行 / 明细 {items_done} 行"
              f"（跳过 无用户{stat_tot['no_user']} 污染{stat_tot['polluted']}"
              + (f" 空码{stat_tot['empty_pkg']} 不匹配{stat_tot['mismatch']}" if not offline else "") + "）")
        return

    last = st["last_id"]
    batch_no = 0
    while True:
        cur.execute(
            f"SELECT * FROM `order` WHERE deleted_at IS NULL AND id > %s{biz_filter} ORDER BY id LIMIT %s",
            (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        if processed:
            rows = [r for r in rows if str(r.get("order_id") or "") not in processed]
        oids = [str(r["order_id"]) for r in rows if r.get("order_id")]
        prod_by_order = {}
        if oids:
            pf = ",".join(["%s"] * len(oids))
            cur.execute(
                f"SELECT * FROM order_product WHERE order_id IN ({pf}) ORDER BY order_id, id", oids)
            for p in cur.fetchall():
                prod_by_order.setdefault(str(p["order_id"]), []).append(p)
        order_ins, item_ins, stat = build(rows, by_account, prod_by_order, now)
        insert_batch(dev_conn, SHADOW_ORDER, order_ins)
        insert_batch(dev_conn, SHADOW_ITEM, item_ins)
        rows_done += len(order_ins)
        items_done += len(item_ins)
        for k in stat_tot:
            stat_tot[k] += stat[k]
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        st_i["rows"] = items_done
        save_state(state)
        batch_no += 1
        if batch_no % 10 == 0:
            print(f"  [{key_o}] 第{batch_no}批: 订单累计{rows_done} / 明细累计{items_done}")
    st["done"] = True
    st_i["done"] = True
    save_state(state)
    print(f"  ✅ {key_o} 迁移完成，共 {rows_done} 行 / 明细 {items_done} 行"
          f"（跳过 无用户{stat_tot['no_user']} 污染{stat_tot['polluted']}"
          + (f" 空码{stat_tot['empty_pkg']} 不匹配{stat_tot['mismatch']}" if not offline else "") + "）")


def main():
    args = sys.argv[1:]
    dev_conn = db(DEV_DB)
    state = load_state()

    if "--init" in args:
        create_shadow_tables(dev_conn)
        print("订单+明细影子表创建完成")
        return
    if "--reset" in args:
        for t in (SHADOW_ORDER, SHADOW_ITEM):
            dev_conn.cursor().execute(f"DROP TABLE IF EXISTS `{t}`")
        dev_conn.commit()
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("已清空订单/明细影子表与状态")
        return

    create_shadow_tables(dev_conn)

    if "--check" in args:
        cur = dev_conn.cursor()
        for t in (SHADOW_ORDER, SHADOW_ITEM):
            cur.execute(f"SELECT COUNT(*) c FROM `{t}`")
            print(f"  {t}: {cur.fetchone()['c']} 行")
        return

    old_conn = db(OLD_DB)

    limit = 0
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
        print(f"试运行模式：仅处理已迁移用户(by_account)的订单")

    offline = "--offline" in args
    if offline and not OFFLINE_ENABLED:
        print("线下迁移开关未开启（MIGRATE_OFFLINE=1 可开启），面对面订单本次不处理")
        return
    if offline:
        print("线下模式：仅迁移面对面(SiteStationWeight)订单，明细 item_code 留空（package 迁移后执行）")

    preload_used_ids(dev_conn)
    preload_recycle_ids(dev_conn)
    preload_order_nos(dev_conn)
    print(f"已预加载 {len(_used_ids)} 个现有 ID + {len(_order_nos)} 个订单号")

    print("加载 account_id -> 新 member_user.id 映射（含线上已存在用户）...")
    by_account = rebuild_by_account(old_conn, dev_conn, load_target_users())
    print(f"  by_account: {len(by_account)} 条")

    migrate_order(old_conn, dev_conn, by_account, state, limit, offline)

    print(f"\n===== 订单迁移自检{'（线下）' if offline else ''} =====")
    cur = dev_conn.cursor()
    for t in (SHADOW_ORDER, SHADOW_ITEM):
        cur.execute(f"SELECT COUNT(*) c FROM `{t}`")
        print(f"  {t}: {cur.fetchone()['c']} 行")
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_ORDER}` WHERE user_id IS NULL")
    print(f"  订单 user_id 为空: {cur.fetchone()['c']}")
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_ITEM}` WHERE order_id IS NULL")
    print(f"  明细 order_id 为空: {cur.fetchone()['c']}")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_ITEM}` i "
        f"LEFT JOIN `{SHADOW_ORDER}` o ON o.id=i.order_id WHERE o.id IS NULL")
    print(f"  明细 order_id 未命中订单: {cur.fetchone()['c']}")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_ITEM}` WHERE item_id<>{ITEM_ID_FIXED} "
        f"OR item_name<>'{ITEM_NAME_FIXED}' OR item_unit<>'{ITEM_UNIT_FIXED}'")
    print(f"  明细固定列不符: {cur.fetchone()['c']}")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_ITEM}` WHERE item_code IS NULL OR item_code=''")
    print(f"  明细 item_code 为空（线下模式预期=线下明细数，线上模式应0）: {cur.fetchone()['c']}")


if __name__ == "__main__":
    main()
