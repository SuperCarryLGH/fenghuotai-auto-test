#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给影子钱包打同步标记：需要 UPDATE（已存在用户继承线上 id 的钱包）置 sync_action='UPDATE'，
其余（新增用户钱包）置 'INSERT'，供同步线上时区分。

- 幂等：先重置全部为 INSERT，再按线上用户 id 集合标记 UPDATE
- 线上用户 id 集合来源：线上 xlsx（member_user sheet 的 id 列），与迁移数据源一致
- sync_action 为临时标记列，同步线上时排除、同步完成后可删

用法：
    .venv/bin/python scripts/mark_sync_action.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from migrate_old_db_to_shadow import db, DEV_DB, XLSX_FILE, XLSX_SHEET_USER


def main():
    dev_conn = db(DEV_DB)
    cur = dev_conn.cursor()

    # 1) 确保 sync_action 列存在
    cur.execute("SHOW COLUMNS FROM shadow_pay_wallet LIKE 'sync_action'")
    if not cur.fetchone():
        cur.execute(
            "ALTER TABLE shadow_pay_wallet "
            "ADD COLUMN sync_action varchar(10) NOT NULL DEFAULT 'INSERT'")
        dev_conn.commit()
        print("已新增临时列 sync_action")

    # 2) 重置（幂等）
    cur.execute("UPDATE shadow_pay_wallet SET sync_action='INSERT'")
    dev_conn.commit()

    # 3) 读线上用户 id 集合（xlsx member_user.id）
    xu = pd.read_excel(XLSX_FILE, sheet_name=XLSX_SHEET_USER, usecols=["id"])
    online_uids = set(int(x) for x in xu["id"].dropna())
    print(f"线上用户 id 集合: {len(online_uids)} 个")

    # 4) 标记已存在用户的钱包为 UPDATE
    fmt = ",".join(["%s"] * len(online_uids))
    cur.execute(
        f"UPDATE shadow_pay_wallet SET sync_action='UPDATE' WHERE user_id IN ({fmt})",
        list(online_uids))
    dev_conn.commit()
    marked = cur.rowcount

    # 5) 报告
    cur.execute("SELECT COUNT(*) n FROM shadow_pay_wallet")
    total = cur.fetchone()["n"]
    cur.execute("SELECT sync_action, COUNT(*) n FROM shadow_pay_wallet GROUP BY sync_action")
    dist = cur.fetchall()
    print(f"\n== 标记结果 ==")
    print(f"  钱包总数: {total}")
    for r in dist:
        print(f"    {r['sync_action']}: {r['n']}")
    print(f"  本次标记 UPDATE: {marked}")
    cur.execute(
        "SELECT id, user_id, sync_action FROM shadow_pay_wallet WHERE sync_action='UPDATE' LIMIT 3")
    print("  UPDATE 样本:", cur.fetchall())
    dev_conn.close()


if __name__ == "__main__":
    main()
