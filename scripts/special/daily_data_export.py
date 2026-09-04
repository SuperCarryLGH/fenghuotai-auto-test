#!/usr/bin/env python3
"""
每日数据导出：从线上 prod 库查询前一天数据，导出为一个 xlsx（两个 sheet）

部署在 Jenkins，凌晨定时跑：
  python daily_data_export.py
  python daily_data_export.py --date 2026-09-01          # 指定日期(补跑)
  python daily_data_export.py --output /path/每日数据.xlsx # 指定输出(建议传 ${WORKSPACE}/每日数据_YYYY-MM-DD.xlsx)

邮件由 Jenkins email-ext 插件发送该 xlsx 附件。
"""
import os
import sys
import argparse
import datetime
import decimal

import pymysql
from openpyxl import Workbook

# ============================================================
# 配置
# ============================================================
PROD_DB = {
    "host": os.getenv("PROD_DB_HOST", "sf-fht-prod.rwlb.rds.aliyuncs.com"),
    "port": int(os.getenv("PROD_DB_PORT", "3306")),
    "user": os.getenv("PROD_DB_USER", "readonly_user"),
    "password": os.getenv("PROD_DB_PASSWORD", "0toGbhBTegP%hDAhh-i"),
    "database": os.getenv("PROD_DB_DATABASE", "fht_yhs"),
}

STATUS_MAP = {10: "待回收", 20: "回收中", 30: "已完成", 50: "已取消"}

PLATFORM_MAP = {
    "smk": "市民卡",
    "szd": "苏周到",
    "szdmini": "苏周到小程序",
    "web": "PC网站",
    "mp-weixin": "微信小程序",
    "h5": "H5网页",
    "mp-alipay": "支付宝小程序",
    "cn": "菜鸟",
    "sfapp": "顺丰APP",
    "sfmini": "顺丰小程序",
}

SQL_ORDER = """
SELECT order_no 订单编号, express_order 物流单号, platform 下单平台, provider 供应商,
       b.id AS 推广记录id, user_name 下单人, user_phone 下单人手机号, a.user_id 下单账户id,
       province 省份, city 城市, district 区域, detail_address 详细地址,
       real_weight 下单重量, a.status 状态
FROM recycle_order a
LEFT JOIN dist_promoter_order_record b ON a.id = b.order_id
WHERE a.create_time >= %s AND a.create_time < %s
"""

SQL_MEMBER = """
SELECT a.id 用户id, a.mobile 手机号, platform 平台, b.id AS 绑定记录id
FROM member_user a
LEFT JOIN dist_promoter_user_relation b ON a.id = b.user_id
WHERE a.create_time >= %s AND a.create_time < %s
"""


def to_plain(v):
    """Decimal 等转成可写单元格的类型；19位雪花ID转字符串保留精度、避免科学计数法"""
    if isinstance(v, decimal.Decimal):
        if v == v.to_integral_value() and abs(v) >= 1e15:
            return str(int(v))
        return float(v)
    if isinstance(v, int) and abs(v) >= 1e15:
        return str(v)
    return v


def run_query(cur, sql, start, end, status_index=None, yesno_indices=None, platform_indices=None):
    """执行查询并做二次处理:
    - status_index: 状态列(转中文)
    - yesno_indices: 有值→"是", 无值→"否" 的列
    - platform_indices: 平台代码→中文, 无值/未知保持原样
    """
    cur.execute(sql, (start, end))
    headers = [d[0] for d in cur.description]
    yesno_indices = yesno_indices or set()
    platform_indices = platform_indices or set()
    rows = []
    for row in cur.fetchall():
        r = [to_plain(x) for x in row]
        if status_index is not None:
            s = r[status_index]
            r[status_index] = STATUS_MAP.get(s, s)
        for idx in yesno_indices:
            r[idx] = "是" if r[idx] is not None and r[idx] != "" else "否"
        for idx in platform_indices:
            if r[idx] is not None and r[idx] != "":
                r[idx] = PLATFORM_MAP.get(r[idx], r[idx])
        rows.append(r)
    return headers, rows


def main():
    ap = argparse.ArgumentParser(description="每日数据导出(线上prod前一天)")
    ap.add_argument("--date", type=str, default=None,
                    help="查询日期 YYYY-MM-DD（默认=运行机日期前一天）")
    ap.add_argument("--output", type=str, default=None,
                    help="输出xlsx路径（默认 ./每日数据_YYYY-MM-DD.xlsx）")
    args = ap.parse_args()

    if args.date:
        date = datetime.date.fromisoformat(args.date)
    else:
        date = datetime.date.today() - datetime.timedelta(days=1)

    start = f"{date} 00:00:00"
    end = f"{date + datetime.timedelta(days=1)} 00:00:00"
    out = args.output or f"./每日数据_{date}.xlsx"

    print(f"查询日期: {date}")
    print(f"时间范围: {start} ~ {end}")
    print(f"输出文件: {out}")
    print("=" * 50)

    try:
        conn = pymysql.connect(charset="utf8mb4", connect_timeout=15,
                               cursorclass=pymysql.cursors.Cursor, **PROD_DB)
    except Exception as e:
        print(f"❌ 连接线上库失败: {e}")
        sys.exit(1)
    cur = conn.cursor()

    wb = Workbook()

    try:
        # Sheet1: 回收订单（状态转中文, 推广记录id转是/否, 下单平台/供应商转中文）
        h1, rows1 = run_query(cur, SQL_ORDER, start, end, status_index=13,
                              yesno_indices={4}, platform_indices={2, 3})
        ws1 = wb.active
        ws1.title = "回收订单"
        ws1.append(h1)
        for r in rows1:
            ws1.append(r)
        print(f"回收订单: {len(rows1)} 行")

        # Sheet2: 会员用户（绑定记录id转是/否, 平台转中文）
        h2, rows2 = run_query(cur, SQL_MEMBER, start, end, yesno_indices={3}, platform_indices={2})
        ws2 = wb.create_sheet("会员用户")
        ws2.append(h2)
        for r in rows2:
            ws2.append(r)
        print(f"会员用户: {len(rows2)} 行")
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)
    finally:
        conn.close()

    wb.save(out)
    print(f"✅ 已导出: {out}")
    print("=" * 50)


if __name__ == "__main__":
    main()