#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包裹迁移脚本（纯 dev 派生，无老库依赖）：shadow_recycle_order_item → shadow_recycle_package_item。

规则（开发代码确认）：
  - 每 1 条 recycle_order_item → 1 条 recycle_package_item（订单过滤已保证明细/包裹 1:1）
  - package_no        = item.item_code（订单 package_code 位置码，跨订单唯一，与 item_code 逐条一致）
  - recycle_order_id  = item.order_id
  - item_id/name/unit/pic = item 的固定 统货/KG / item_pic
  - recycle_price/weight/total_price = item.price / item.weight / item.total_price
  - recycle_time / recycle_recive_time / recycle_pay_time = order.create_time / receive_time / pay_time(NULL)
  - 状态：package_status=101、stock_status=0、transfer_status=0（固定）
    动态（按订单状态，开发确认）：
      inspect_status: 订单 inspect_status=20(已质检待审核) → 30(已质检审核通过)；否则 10(待质检)
      settle_status : 订单 settlement_status=30(已结算) → 1(已结算)；否则 0(未结算)
  - creator/updater='migrate'、create_time=order.create_time、update_time=now、deleted=0、tenant_id=1
  - 其余 clear/transfer/inspect/stock 明细列 → NULL（不填）

防冲突：preload dev recycle_package_item 现有 package_no（含种子 1338 条），命中（理论为0）→ 跳过计数。

用法：
    python scripts/migrate_package_item.py --init       # 只建影子表
    python scripts/migrate_package_item.py --reset      # 清空影子表+状态
    python scripts/migrate_package_item.py --limit N    # 试运行：前N条
    python scripts/migrate_package_item.py              # 全量（断点续传）
    python scripts/migrate_package_item.py --check      # 查看影子表行数
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

SHADOW_TABLE = "shadow_recycle_package_item"
ITEM_TABLE = "shadow_recycle_order_item"
ORDER_TABLE = "shadow_recycle_order"
STATE_FILE = PROJECT_ROOT / "scripts" / ".migrate_package_item_state.json"

PACKAGE_STATUS = 101        # 清运中/回收待到仓（开发代码值）
STOCK_STATUS = 0            # 未入库（保持）
TRANSFER_STATUS = 0         # NOT NULL
# 动态（按订单状态，开发确认）：
#   settle_status : 订单 settlement_status=30(已结算) → 1(已结算)，否则 0(未结算)
#   inspect_status: 订单 inspect_status=20(已质检待审核) → 30(已质检审核通过)，否则 10(待质检)


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
    cur.execute(f"CREATE TABLE `{SHADOW_TABLE}` LIKE recycle_package_item")
    conn.commit()
    print(f"  ✅ 创建影子表 {SHADOW_TABLE} (like recycle_package_item)")


def check_complete(conn, rows_done):
    if rows_done <= 0:
        return
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}`")
    actual = cur.fetchone()["c"]
    if actual < rows_done:
        raise SystemExit(
            f"[完整校验失败] {SHADOW_TABLE} 实际{actual} < 已迁移{rows_done}，请 --reset 重跑")


def preload_package_nos(dev_conn):
    """dev recycle_package_item 现有 package_no（含种子），供防冲突"""
    cur = dev_conn.cursor()
    cur.execute("SELECT package_no FROM recycle_package_item")
    return {str(r["package_no"]) for r in cur.fetchall()}


def map_package(item, pkg_id, o_time, now):
    """recycle_order_item 行 + 订单信息 → recycle_package_item 行"""
    # 动态状态（按订单，开发确认）：
    #   inspect_status: 订单已质检待审核(20) → 30(审核通过)，否则 10(待质检)
    #   settle_status : 订单已结算(30) → 1(已结算)，否则 0(未结算)
    inspect_status = 30 if o_time.get("inspect_status") == 20 else 10
    settle_status = 1 if o_time.get("settlement_status") == 30 else 0
    return {
        "id": pkg_id,
        "package_no": item.get("item_code"),                 # = item_code（唯一）
        "package_status": PACKAGE_STATUS,
        "inspect_status": inspect_status,
        "settle_status": settle_status,
        "stock_status": STOCK_STATUS,
        "transfer_status": TRANSFER_STATUS,
        "item_id": item.get("item_id"),
        "item_name": item.get("item_name"),
        "item_unit": item.get("item_unit"),
        "item_pic_url": None,                            # 统一 NULL（开发确认）
        "recycle_price": item.get("price"),
        "recycle_weight": item.get("weight"),
        "recycle_total_price": item.get("total_price"),
        "recycle_time": o_time.get("create_time"),
        "recycle_recive_time": o_time.get("receive_time"),
        "recycle_pay_time": o_time.get("pay_time"),          # = 订单 pay_time（=recycle_end_time）
        "recycle_order_id": item.get("order_id"),
        "creator": "migrate",
        "create_time": o_time.get("create_time") or now,
        "updater": "migrate",
        "update_time": now,
        "deleted": b"\x00",
        "tenant_id": 1,
    }


def migrate_package(dev_conn, state, limit=0):
    key = "recycle_package_item"
    st = state.get(key, {"last_id": 0, "rows": 0, "done": False})
    if st["done"]:
        print("  recycle_package_item 已迁移完成，跳过")
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
    used_nos = preload_package_nos(dev_conn)
    print(f"  [防冲突] dev 现有 package_no {len(used_nos)} 条")

    rows_done = st["rows"]
    last = st["last_id"]
    skipped_collision = 0
    batch_no = 0
    while True:
        cur.execute(
            f"SELECT i.*, o.create_time AS o_create_time, o.receive_time AS o_receive_time, "
            f"o.pay_time AS o_pay_time, o.settlement_status AS o_settlement_status, "
            f"o.inspect_status AS o_inspect_status "
            f"FROM `{ITEM_TABLE}` i LEFT JOIN `{ORDER_TABLE}` o ON o.id = i.order_id "
            f"WHERE i.id > %s ORDER BY i.id LIMIT %s", (last, BATCH))
        rows = cur.fetchall()
        if not rows:
            break
        to_insert = []
        for r in rows:
            pno = r.get("item_code")
            if not pno or pno in used_nos:
                skipped_collision += 1
                continue
            used_nos.add(pno)
            o_time = {
                "create_time": r.get("o_create_time"),
                "receive_time": r.get("o_receive_time"),
                "pay_time": r.get("o_pay_time"),
                "settlement_status": r.get("o_settlement_status"),
                "inspect_status": r.get("o_inspect_status"),
            }
            to_insert.append(map_package(r, gen_id(), o_time, now))
        insert_batch(dev_conn, SHADOW_TABLE, to_insert)
        rows_done += len(to_insert)
        last = rows[-1]["id"]
        st["last_id"] = last
        st["rows"] = rows_done
        save_state(state)
        batch_no += 1
        if batch_no % 10 == 0:
            print(f"  [recycle_package_item] 第{batch_no}批: 累计{rows_done}")
        if limit and rows_done >= limit:
            break
    if not limit:
        st["done"] = True
    save_state(state)
    print(f"  ✅ recycle_package_item 迁移完成，共 {rows_done} 行（跳过冲突 {skipped_collision}）")


def main():
    args = sys.argv[1:]
    dev_conn = db(DEV_DB)
    state = load_state()

    if "--init" in args:
        create_shadow_table(dev_conn)
        print("包裹影子表创建完成")
        return
    if "--reset" in args:
        dev_conn.cursor().execute(f"DROP TABLE IF EXISTS `{SHADOW_TABLE}`")
        dev_conn.commit()
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("已清空包裹影子表与状态")
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
        print(f"试运行模式：仅处理前 {limit} 条明细")

    preload_used_ids(dev_conn)
    print(f"已预加载 {len(_used_ids)} 个现有 ID")

    migrate_package(dev_conn, state, limit)

    print("\n===== 包裹自检 =====")
    cur = dev_conn.cursor()
    cur.execute(f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}`")
    print(f"  {SHADOW_TABLE}: {cur.fetchone()['c']} 行")
    cur.execute(f"SELECT COUNT(*) c, COUNT(DISTINCT package_no) d FROM `{SHADOW_TABLE}`")
    r = cur.fetchone()
    print(f"  package_no 唯一: {'是' if r['c'] == r['d'] else '否'} ({r['c']}/{r['d']})")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}` p "
        f"LEFT JOIN `{ORDER_TABLE}` o ON o.id=p.recycle_order_id WHERE o.id IS NULL")
    print(f"  recycle_order_id 未命中订单: {cur.fetchone()['c']}")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}` WHERE package_status<>{PACKAGE_STATUS} "
        f"OR stock_status<>{STOCK_STATUS} OR transfer_status<>{TRANSFER_STATUS}")
    print(f"  固定列(package/stock/transfer)不符: {cur.fetchone()['c']}")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}` p "
        f"LEFT JOIN `{ORDER_TABLE}` o ON o.id=p.recycle_order_id "
        f"WHERE NOT ((p.inspect_status=30 AND o.inspect_status=20) OR (p.inspect_status=10 AND (o.inspect_status IS NULL OR o.inspect_status<>20))) "
        f"OR NOT ((p.settle_status=1 AND o.settlement_status=30) OR (p.settle_status=0 AND (o.settlement_status IS NULL OR o.settlement_status<>30)))")
    print(f"  动态状态(inspect/settle)与订单不一致: {cur.fetchone()['c']}")
    cur.execute(
        f"SELECT COUNT(*) c FROM `{SHADOW_TABLE}` WHERE package_no IS NULL OR package_no=''")
    print(f"  package_no 为空: {cur.fetchone()['c']}")


if __name__ == "__main__":
    main()
