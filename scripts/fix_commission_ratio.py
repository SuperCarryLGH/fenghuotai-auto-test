#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复线上分佣比例误配（rate 100倍偏高：50→0.5、10→0.1 等）——只读查询 + 生成 SQL，不执行写库。

问题：分佣比例配置写错，price = order_total_price × 错误rate（100倍偏高）。
修复口径（开发确认）：
  - 受影响流水：rate>1 且 remark LIKE '%订单佣金%'
  - 未提现账户（total_expend=0）：balance/total_income 各减多记（余额非负）
  - 提现账户（total_expend>0）：balance/total_income 各减多记（余额直接扣成负的）
  - 流水修正：rate→rate/100，price→FLOOR(price/100)（已验证 = FLOOR(order_total_price*rate/100)）

输出两份 SQL：
  /Users/rs/Documents/fix_commission_ratio.sql            （未提现账户）
  /Users/rs/Documents/fix_commission_ratio_withdrawn.sql  （提现账户，余额可为负）

用法：.venv/bin/python scripts/fix_commission_ratio.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pymysql import connect
from pymysql.cursors import DictCursor

PROD = dict(host="sf-fht-prod.rwlb.rds.aliyuncs.com", port=3306,
            user="readonly_user", password="0toGbhBTegP%hDAhh-i", database="fht_yhs")
MARK = "migrate_fix_ratio"


def gen(conn, expend_cmp, tag, out):
    """生成一份修复 SQL；expend_cmp: 账户 total_expend 过滤条件（'=0' 或 '>0'）"""
    ACCOUNT_WHERE = (f"total_expend{expend_cmp} AND id IN ("
                     "SELECT DISTINCT commission_account_id FROM dist_commission_record "
                     "WHERE rate>1 AND remark LIKE '%订单佣金%')")
    RECORD_WHERE = (f"rate>1 AND remark LIKE '%订单佣金%' AND commission_account_id IN ("
                    f"SELECT id FROM dist_commission_account WHERE total_expend{expend_cmp})")

    cur = conn.cursor()
    cur.execute(f"SELECT id, commission_account_id, price, rate, order_total_price "
                f"FROM dist_commission_record WHERE {RECORD_WHERE} ORDER BY id")
    records = cur.fetchall()
    for r in records:
        r["price_new"] = int(r["price"]) // 100          # FLOOR(price/100)
        r["rate_new"] = float(r["rate"]) / 100
        r["overpaid"] = int(r["price"]) - r["price_new"]

    cur.execute(f"SELECT id, account_id, balance, total_income, total_expend, total_freeze "
                f"FROM dist_commission_account WHERE {ACCOUNT_WHERE} ORDER BY id")
    accounts = cur.fetchall()
    acc_over = {}
    for r in records:
        acc_over[r["commission_account_id"]] = acc_over.get(r["commission_account_id"], 0) + r["overpaid"]
    for a in accounts:
        a["overpaid"] = acc_over.get(a["id"], 0)
        a["bal_new"] = int(a["balance"] or 0) - a["overpaid"]
        a["inc_new"] = int(a["total_income"] or 0) - a["overpaid"]

    total_over = sum(r["overpaid"] for r in records)
    neg_cnt = sum(1 for a in accounts if a["bal_new"] < 0)
    lines = []
    w = lines.append
    w("-- ============================================================")
    w(f"-- 线上分佣比例误配修复 SQL（{tag}）——只读脚本自动生成")
    w("-- 问题：rate 从 0.5/0.1 误写成 50/10，price 按 order_total_price×rate 计算，100倍偏高")
    w(f"-- 口径（开发确认）：{tag} + rate>1且remark含'订单佣金'的流水")
    w("-- 修复：流水 rate→rate/100、price→FLOOR(price/100)；账户 balance/total_income 减多记")
    if expend_cmp == ">0":
        w("-- ⚠️ 已提现账户：余额直接扣成负的（开发确认）")
    w(f"-- 影响：流水 {len(records)} 条 / 账户 {len(accounts)} 个 / 多记总额 {total_over:,} 分 = {total_over/100:,.2f} 元"
      + (f" / 扣减后余额为负 {neg_cnt} 个" if expend_cmp == ">0" else ""))
    w("-- ⚠️ 执行前请先核对以下 SELECT；执行后跑验证 SELECT")
    w("-- ============================================================")
    w("")
    w("-- ---------- ① 修复前核对（应返回上面数字）----------")
    w(f"SELECT COUNT(*) AS 受影响流水, SUM(price) AS 现价总分 FROM dist_commission_record WHERE {RECORD_WHERE};")
    w(f"SELECT COUNT(*) AS 受影响账户 FROM dist_commission_account WHERE {ACCOUNT_WHERE};")
    w("")
    w(f"-- ---------- ② 修复流水（{len(records)}条）----------")
    for r in records:
        w(f"UPDATE dist_commission_record SET rate={r['rate_new']:.2f}, "
          f"price={r['price_new']}, updater='{MARK}', update_time=NOW() "
          f"WHERE id={r['id']};")
    w("")
    w(f"-- ---------- ③ 修复账户余额/收入（{len(accounts)}个）----------")
    for a in accounts:
        w(f"UPDATE dist_commission_account SET balance={a['bal_new']}, "
          f"total_income={a['inc_new']}, updater='{MARK}', update_time=NOW() "
          f"WHERE id={a['id']};")
    w("")
    w("-- ---------- ④ 修复后验证（应全为0）----------")
    w(f"SELECT COUNT(*) AS rate残留 FROM dist_commission_record WHERE {RECORD_WHERE};")
    w(f"SELECT COUNT(*) AS 流水价格不符 FROM dist_commission_record "
      f"WHERE {RECORD_WHERE} AND price <> FLOOR(order_total_price*rate);")
    w(f"SELECT COUNT(*) AS 账户余额不符 FROM dist_commission_account a "
      f"WHERE {ACCOUNT_WHERE} AND a.balance <> a.total_income - a.total_expend - a.total_freeze;")

    Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    dist = {}
    for r in records:
        dist.setdefault((r["rate"], r["rate_new"]), 0)
        dist[(r["rate"], r["rate_new"])] += 1
    print(f"✅ {out}")
    print(f"   {tag}: 流水 {len(records)} 条 | 账户 {len(accounts)} 个 | 多记 {total_over:,} 分 = {total_over/100:,.2f} 元"
          + (f" | 扣负 {neg_cnt} 个" if expend_cmp == ">0" else ""))
    print(f"   rate 分布: " + ", ".join(f"{k[0]}->{k[1]:.2f}({v}条)" for k, v in sorted(dist.items())))
    return len(records), len(accounts)


def main():
    c = connect(cursorclass=DictCursor, charset="utf8mb4", connect_timeout=10, **PROD)
    n1, a1 = gen(c, "=0", "未提现账户(total_expend=0)", "/Users/rs/Documents/fix_commission_ratio.sql")
    n2, a2 = gen(c, ">0", "提现账户(total_expend>0)", "/Users/rs/Documents/fix_commission_ratio_withdrawn.sql")
    c.close()
    print(f"\n总计：流水 {n1+n2} 条 / 账户 {a1+a2} 个")
    print("文件：fix_commission_ratio.sql（未提现） + fix_commission_ratio_withdrawn.sql（提现）")


if __name__ == "__main__":
    main()