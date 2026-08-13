#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据导出：把指定迁移用户（影子表）的全部数据导入 dev 真实表，供端上业务逻辑测试。

- 每个用户的全部相关数据跨 9 张表导入（用户/钱包/流水/地址/订单/明细/包裹/分销/关系）
- 临时列（shadow 有、dev 真实表没有的列）自动排除：member_user.operation_center_uuid、
  pay_wallet.sync_action、recycle_order.operation_center_uuid/order_id_old
- 幂等：按主键 id 已在目标表则跳过；order_no/package_no 冲突会报告
- 按 FK 顺序插入：用户→钱包→流水→地址→订单→明细→包裹→分销→关系

用法：
    .venv/bin/python scripts/export_users_for_test.py                     # 默认 3 个候选用户
    .venv/bin/python scripts/export_users_for_test.py <uid1> <uid2> ...   # 指定用户id
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pymysql.cursors import DictCursor

from migrate_old_db_to_shadow import db, DEV_DB

# 默认候选用户（数据全：9995=推广员+1705关系 / 6966=49订单 / 8282=29地址）
DEFAULT_USERS = [2087124692782546972, 2087124044020187203, 2087123874201206859]

# (影子表, dev真实表, 该用户的关联条件模板)
TABLES = [
    ("shadow_member_user", "member_user", lambda uid: "id=%s", (lambda uid: [uid])),
    ("shadow_pay_wallet", "pay_wallet", lambda uid: "user_id=%s", (lambda uid: [uid])),
    ("shadow_member_address", "member_address", lambda uid: "user_id=%s", (lambda uid: [uid])),
    ("shadow_recycle_order", "recycle_order", lambda uid: "user_id=%s", (lambda uid: [uid])),
    ("shadow_dist_promoter", "dist_promoter", lambda uid: "user_id=%s", (lambda uid: [uid])),
    ("shadow_dist_promoter_user_relation", "dist_promoter_user_relation",
     lambda uid: "(user_id=%s OR promotor_user_id=%s)", (lambda uid: [uid, uid])),
]

# 依赖上一步结果的表（钱包→流水 / 订单→明细→包裹）
DEP_TABLES = [
    ("shadow_pay_wallet_transaction", "pay_wallet_transaction", "wallet_id", "shadow_pay_wallet", "user_id"),
    ("shadow_recycle_order_item", "recycle_order_item", "order_id", "shadow_recycle_order", "user_id"),
    ("shadow_recycle_package_item", "recycle_package_item", "recycle_order_id", "shadow_recycle_order", "user_id"),
]

_cols_cache = {}


def real_cols(conn, table):
    if table not in _cols_cache:
        cur = conn.cursor()
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        _cols_cache[table] = [r["Field"] for r in cur.fetchall()]
    return set(_cols_cache[table])


def insert_idempotent(conn, target, rows, pk="id"):
    """把 rows(字典列表) 插入 target；已存在主键跳过；返回 (插入, 已存在)"""
    if not rows:
        return 0, 0
    cols = [c for c in rows[0].keys() if c in real_cols(conn, target)]
    if not cols:
        return 0, 0
    ids = [r[pk] for r in rows]
    cur = conn.cursor()
    fmt = ",".join(["%s"] * len(ids))
    cur.execute(f"SELECT `{pk}` FROM `{target}` WHERE `{pk}` IN ({fmt})", ids)
    existing = {int(r[pk]) for r in cur.fetchall()}
    to_insert = [r for r in rows if int(r[pk]) not in existing]
    if to_insert:
        ck = ", ".join(f"`{c}`" for c in cols)
        ph = ", ".join(["%s"] * len(cols))
        cur.executemany(
            f"INSERT INTO `{target}` ({ck}) VALUES ({ph})",
            [tuple(r[c] for c in cols) for r in to_insert])
        conn.commit()
    return len(to_insert), len(rows) - len(to_insert)


def main():
    args = sys.argv[1:]
    users = [int(a) for a in args] if args else DEFAULT_USERS
    print(f"== 导出测试用户 {len(users)} 个: {users} ==")
    conn = db(DEV_DB)
    cur = conn.cursor()

    summary = []
    for uid in users:
        print(f"\n===== 用户 {uid} =====")
        u_total = 0
        # 钱包/订单 id 收集（供流水/明细/包裹用）
        cur.execute("SELECT id FROM shadow_pay_wallet WHERE user_id=%s", (uid,))
        wallet_ids = [int(r["id"]) for r in cur.fetchall()]
        cur.execute("SELECT id FROM shadow_recycle_order WHERE user_id=%s", (uid,))
        order_ids = [int(r["id"]) for r in cur.fetchall()]

        def show(src, target, where, wargs):
            nonlocal u_total
            cur.execute(f"SELECT * FROM `{src}` WHERE {where}", wargs)
            rows = cur.fetchall()
            ins, exist = insert_idempotent(conn, target, rows)
            u_total += ins
            print(f"  {target}: 导入 {ins} / 已存在跳过 {exist}")
            return rows

        show("shadow_member_user", "member_user", "id=%s", [uid])
        show("shadow_pay_wallet", "pay_wallet", "user_id=%s", [uid])
        show("shadow_member_address", "member_address", "user_id=%s", [uid])
        show("shadow_recycle_order", "recycle_order", "user_id=%s", [uid])

        if wallet_ids:
            f = ",".join(["%s"] * len(wallet_ids))
            show("shadow_pay_wallet_transaction", "pay_wallet_transaction",
                 f"wallet_id IN ({f})", wallet_ids)
        if order_ids:
            f = ",".join(["%s"] * len(order_ids))
            show("shadow_recycle_order_item", "recycle_order_item", f"order_id IN ({f})", order_ids)
            show("shadow_recycle_package_item", "recycle_package_item",
                 f"recycle_order_id IN ({f})", order_ids)
        prom = show("shadow_dist_promoter", "dist_promoter", "user_id=%s", [uid])
        rels = show("shadow_dist_promoter_user_relation", "dist_promoter_user_relation",
                    "(user_id=%s OR promotor_user_id=%s)", [uid, uid])

        # 报告悬空引用
        if rels:
            dangling_prom = sum(1 for r in rels if r.get("promoter_id") and int(r["promoter_id"]) not in
                                {x["id"] for x in prom})
            print(f"  ⚠️ 关系表 promoter_id 指向未导入推广员: {dangling_prom}（含非本次用户）")
        summary.append((uid, u_total))

    print("\n===== 汇总 =====")
    for uid, n in summary:
        print(f"  用户 {uid}: 共导入 {n} 行")
    conn.close()


if __name__ == "__main__":
    main()
