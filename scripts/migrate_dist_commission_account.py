#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佣金账户迁移脚本（纯 dev 派生，无老库依赖）：shadow_dist_promoter → shadow_dist_commission_account。

规则（开发确认，2026-08）：
  - 每 1 条 dist_promoter → 1 条佣金账户（1:1）
  - id            : snowflake
  - account_type  : 固定 1
  - account_id    : dist_promoter.id（该推广员的佣金账户）
  - balance/total_income/total_expend/total_freeze : 0
  - remark        : NULL
  - creator/updater : 'migrate'
  - create_time   : dist_promoter.create_time
  - update_time   : dist_promoter.update_time
  - deleted=0、tenant_id=1
  - dev 唯一索引 (account_type, account_id)：account_id=dist_promoter.id（PK 唯一）→ 天然 1:1

用法：
    python scripts/migrate_dist_commission_account.py --init       # 只建影子表
    python scripts/migrate_dist_commission_account.py --reset      # 清空影子表+状态
    python scripts/migrate_dist_commission_account.py --limit N    # 试运行：前N条
    python scripts/migrate_dist_commission_account.py              # 全量（断点续传）
    python scripts/migrate_dist_commission_account.py --check      # 查看影子表行数
"""
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pymysql.cursors import DictCursor  # noqa: E402

from migrate_old_db_to_shadow import (  # noqa: E402
    db, DEV_DB, BATCH, gen_id, insert_batch, preload_used_ids, _used_ids,
)

SHADOW_TABLE = "shadow_dist_commission_account"
SRC_TABLE = "shadow_dist_promoter"
STATE_FILE = PROJECT_ROOT / "scripts" / ".migrate_commission_state.json"

ACCOUNT_TYPE = 1


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def create_shadow_table(conn):
    cur = conn.cursor()
    cur.execute("SHOW TABLES LIKE %s", (SHADOW_TABLE,))
    if cur.fetchone():
        print(f"  影子表已存在: {SHADOW_TABLE}")
        return
    cur.execute(f"CREATE TABLE `{SHADOW_TABLE}` LIKE dist_commission_account")
    conn.commit()
    print(f"  ✅ 创建影子表 {SHADOW_TABLE} (like dist_commission_account)")


def check_complete(conn, rows_done):
    if rows_done <= 0:
        return
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}`")
    actual = cur.fetchone()["c"]
    if actual < rows_done:
        raise SystemExit(
            f"[完整校验失败] {SHADOW_TABLE} 实际{actual} < 已迁移{rows_done}，请 --reset 重跑")


def preload_account_ids(dev_conn):
    """dev dist_commission_account 现有 account_id（防重跑冲突）"""
    cur = dev_conn.cursor()
    cur.execute("SELECT account_id FROM dist_commission_account")
    return {int(r["account_id"]) for r in cur.fetchall()}


def map_account(p, acc_id, now):
    return {
        "id": acc_id,
        "account_type": ACCOUNT_TYPE,
        "account_id": p.get("id"),                 # dist_promoter.id
        "balance": 0,
        "total_income": 0,
        "total_expend": 0,
        "total_freeze": 0,
        "remark": None,
        "creator": "migrate",
        "create_time": p.get("create_time") or now,
        "updater": "migrate",
        "update_time": p.get("update_time") or now,
        "deleted": b"\x00",
        "tenant_id": 1,
    }


def migrate_commission(dev_conn, state, limit=0):
    key = "dist_commission_account"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  dist_commission_account 已迁移完成，跳过")
        return
    check_complete(dev_conn, st["rows"])

    if st.get("last_id", 0) == 0:
        cur_c = dev_conn.cursor()
        cur_c.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}`")
        if cur_c.fetchone()["c"] > 0:
            raise SystemExit(
                f"[保护] {SHADOW_TABLE} 已有数据但无断点，请先 --reset 再全量")

    cur = dev_conn.cursor()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    used = preload_account_ids(dev_conn)
    print(f"  [防冲突] dev 现有 account_id {len(used)} 条")

    rows_done = st["rows"]
    last = st["last_id"]
    skipped_collision = 0
    batch_no = 0
    while True:
        cur.execute(
            f"SELECT id, create_time, update_time FROM `{SRC_TABLE}` "
            f"WHERE id > %s ORDER BY id LIMIT %s", (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        to_insert = []
        for r in rows:
            if r["id"] in used:
                skipped_collision += 1
                continue
            used.add(r["id"])
            to_insert.append(map_account(r, gen_id(), now))
        insert_batch(dev_conn, SHADOW_TABLE, to_insert)
        rows_done += len(to_insert)
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        save_state(state)
        batch_no += 1
        if batch_no % 10 == 0:
            print(f"  [dist_commission_account] 第{batch_no}批: 累计{rows_done}")
        if limit and rows_done >= limit:
            break
    if not limit:
        st["done"] = True
    save_state(state)
    print(f"  ✅ dist_commission_account 迁移完成，共 {rows_done} 行（跳过冲突 {skipped_collision}）")


def main():
    args = sys.argv[1:]
    dev_conn = db(DEV_DB)
    state = load_state()

    if "--init" in args:
        create_shadow_table(dev_conn)
        print("佣金账户影子表创建完成")
        return
    if "--reset" in args:
        dev_conn.cursor().execute(f"DROP TABLE IF EXISTS `{SHADOW_TABLE}`")
        dev_conn.commit()
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("已清空佣金账户影子表与状态")
        return

    create_shadow_table(dev_conn)

    if "--check" in args:
        cur = dev_conn.cursor()
        cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}`")
        print(f"  {SHADOW_TABLE}: {cur.fetchone()['c']} 行")
        return

    limit = 0
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
        print(f"试运行模式：仅处理前 {limit} 条推广员")

    preload_used_ids(dev_conn)
    print(f"已预加载 {len(_used_ids)} 个现有 ID")

    migrate_commission(dev_conn, state, limit)

    print("\n===== 佣金账户自检 =====")
    cur = dev_conn.cursor()
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}`")
    print(f"  {SHADOW_TABLE}: {cur.fetchone()['c']} 行")
    cur.execute(
        f"SELECT COUNT(*) c, COUNT(DISTINCT account_id) d, COUNT(DISTINCT (account_type*1000000000000+account_id)) u FROM `{SHADOW_TABLE}`")
    r = cur.fetchone()
    print(f"  account_id 唯一: {'是' if r['c'] == r['d'] else '否'} ({r['c']}/{r['d']})")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}` WHERE account_type<>{ACCOUNT_TYPE} "
        f"OR balance<>0 OR total_income<>0 OR total_expend<>0 OR total_freeze<>0")
    print(f"  account_type/金额固定值不符: {cur.fetchone()['c']}")


if __name__ == "__main__":
    main()
