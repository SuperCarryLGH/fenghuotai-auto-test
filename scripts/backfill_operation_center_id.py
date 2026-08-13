#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后置脚本：按线上分拣中心映射表（老系统id UUID → 新系统id），回填 operation_center_id。

回填对象（均从临时列 operation_center_uuid 读老 UUID）：
  shadow_member_user.operation_center_id    ← 老 sys_user.pay_station_id
  shadow_recycle_order.operation_center_id  ← 老 order.operation_center_id

- 匹配键：老系统id(UUID) 精确匹配（本地模拟库无 station 表也能跑，不依赖名字）
- 不匹配的行：不处理（operation_center_id 保持现状）
- 幂等：只更新能匹配的行，重复运行结果一致
- 关键：新系统id 为 19 位 snowflake，必须按字符串读 xlsx（dtype=str），
  否则 pandas 按 float 读会精度丢失（超出 2^53 精确范围）
- 临时列同步线上时排除

用法：
    .venv/bin/python scripts/backfill_operation_center_id.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from migrate_old_db_to_shadow import db, DEV_DB

XLSX_MAPPING = "/Users/rs/Documents/线上分拣中心.xlsx"
TEMP_COL = "operation_center_uuid"
TARGET_COL = "operation_center_id"
TABLES = ["shadow_member_user", "shadow_recycle_order"]


def load_mapping():
    """读映射表，返回 {老系统id(UUID): int(新系统id)}；新系统id 按字符串读防精度丢失"""
    df = pd.read_excel(XLSX_MAPPING, dtype={"老系统id": str, "新系统id": str})
    mapping = {}
    for _, r in df.iterrows():
        uid = str(r["老系统id"]).strip()
        nid = str(r["新系统id"]).strip()
        if not uid or not nid.isdigit():
            print(f"  ⚠️ 跳过无效行: 老id={uid!r} 新id={nid!r}")
            continue
        if len(nid) != 19:
            print(f"  ⚠️ 新id长度异常({len(nid)}): {nid}（疑似 pandas 精度丢失）")
        mapping[uid] = int(nid)
    return mapping


def main():
    print("== 读取线上分拣中心映射 ==")
    mapping = load_mapping()
    print(f"  映射条数: {len(mapping)}")

    dev_conn = db(DEV_DB)
    cur = dev_conn.cursor()

    for table in TABLES:
        # 临时列不存在（未迁移/旧结构）→ 跳过
        cur.execute(f"SHOW COLUMNS FROM `{table}` LIKE '{TEMP_COL}'")
        if not cur.fetchone():
            print(f"  ⚠️ {table} 无临时列 {TEMP_COL}（未迁移或旧结构），跳过")
            continue

        print(f"\n== 回填 {table} ==")
        total = 0
        for uid, nid in mapping.items():
            cur.execute(
                f"UPDATE `{table}` SET `{TARGET_COL}`=%s WHERE `{TEMP_COL}`=%s", (nid, uid))
            total += cur.rowcount
        dev_conn.commit()

        # 未匹配报告：有 UUID 但不在映射表
        if mapping:
            fmt = ",".join(["%s"] * len(mapping))
            cur.execute(
                f"SELECT COUNT(*) n FROM `{table}` "
                f"WHERE `{TEMP_COL}` IS NOT NULL AND `{TEMP_COL}`<>'' "
                f"AND `{TEMP_COL}` NOT IN ({fmt})", list(mapping.keys()))
            remain = cur.fetchone()["n"]
        else:
            remain = None
        cur.execute(f"SELECT COUNT(*) n FROM `{table}` WHERE `{TARGET_COL}` IS NOT NULL")
        filled = cur.fetchone()["n"]

        print(f"  成功回填: {total}")
        if remain is not None:
            print(f"  有UUID但未命中映射(保持现状): {remain}")
        print(f"  {TARGET_COL} 已填总数: {filled}")

    dev_conn.close()


if __name__ == "__main__":
    main()
