#!/usr/bin/env python3
"""
每日数据导出：从线上 prod 库查询前一天数据，导出为一个 xlsx（两个 sheet）
所有转换(平台/供应商/状态/是否推广/推广员/上级)已下沉到 SQL，Python 只执行+写表

部署在 Jenkins，凌晨定时跑：
  python daily_data_export.py
  python daily_data_export.py --date 2026-09-13          # 指定日期(补跑)
  python daily_data_export.py --output /path/每日数据.xlsx
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

# 指定活动（推广平台/渠道/场景 及 会员活动记录）
ACTIVITY_ID = 2097239541775462402

SQL_ORDER = """
SELECT a.order_no 订单编号, a.express_order 物流单号,
  CASE a.platform WHEN 'web' THEN 'H5' WHEN 'mp-weixin' THEN '微信小程序'
    WHEN 'mp-alipay' THEN '支付宝小程序' ELSE '' END AS 下单平台,
  CASE a.provider WHEN 'smk' THEN '市民卡' WHEN 'szd' THEN '苏周到app'
    WHEN 'szdmini' THEN '苏周到小程序' WHEN 'sfmini' THEN '顺丰小程序'
    WHEN 'sfapp' THEN '顺丰app' ELSE '逸回收平台' END AS 供应商,
  CASE WHEN b.id > 0 THEN '是' ELSE '否' END AS 是否推广,
  m.mobile 推广员手机号, mu2.mobile 推广员上级手机号, a.user_id 下单账户id,
  a.user_name 下单人, a.user_phone 下单人手机号,
  a.province 省份, a.city 城市, a.district 区域,
  REPLACE(REPLACE(a.detail_address, CHAR(10), ''), CHAR(13), '') AS 详细地址,
  a.real_weight 下单重量,
  CASE a.status WHEN 10 THEN '待回收' WHEN 20 THEN '回收中'
    WHEN 30 THEN '已完成' WHEN 50 THEN '已取消' END AS 状态,
  a.create_time AS 下单时间, a.receive_time 接单时间, a.pay_time 支付时间,
  d.id AS 活动id, d.`name` AS 活动名字,
  sd1.label AS 推广平台, sd2.label AS 推广渠道, sd3.label AS 推广场景
FROM recycle_order a
LEFT JOIN dist_promoter_order_record b ON a.id = b.order_id
LEFT JOIN dist_promoter c ON c.id = b.promoter_id
LEFT JOIN member_user m ON m.id = c.user_id
LEFT JOIN dist_promoter_user_relation rm ON rm.user_id = m.id
LEFT JOIN member_user mu2 ON mu2.id = rm.promotor_user_id
LEFT JOIN activity d ON d.id = a.activity_id
LEFT JOIN station_cooperation s ON s.id = a.cid
LEFT JOIN system_dict_data sd1 ON sd1.`value` = s.platform COLLATE utf8mb4_0900_ai_ci
LEFT JOIN system_dict_data sd2 ON sd2.`value` = s.channel COLLATE utf8mb4_0900_ai_ci
LEFT JOIN system_dict_data sd3 ON sd3.`value` = s.scene COLLATE utf8mb4_0900_ai_ci
WHERE a.create_time >= %s AND a.create_time < %s
ORDER BY a.create_time ASC
"""

SQL_MEMBER = """
SELECT a.id 用户id, a.mobile 手机号,
  CASE a.platform WHEN 'web' THEN 'H5' WHEN 'mp-weixin' THEN '微信小程序'
    WHEN 'mp-alipay' THEN '支付宝小程序' ELSE '' END AS 注册平台,
  CASE a.provider WHEN 'smk' THEN '市民卡' WHEN 'szd' THEN '苏周到app'
    WHEN 'szdmini' THEN '苏周到小程序' WHEN 'sfmini' THEN '顺丰小程序'
    WHEN 'sfapp' THEN '顺丰app' ELSE '逸回收平台' END AS 注册供应商,
  CASE WHEN b.id > 0 THEN '是' ELSE '否' END AS 是否推广,
  c.mobile 推广员手机号, c2.mobile 推广员上级手机号, a.create_time 注册时间,
  f.id 活动id, f.`name` AS 活动名字,
  sd1.label AS 推广平台, sd2.label AS 推广渠道, sd3.label AS 推广场景
FROM member_user a
LEFT JOIN dist_promoter_user_relation b ON a.id = b.user_id
LEFT JOIN member_user c ON c.id = b.promotor_user_id
LEFT JOIN dist_promoter_user_relation b2 ON b2.user_id = c.id
LEFT JOIN member_user c2 ON c2.id = b2.promotor_user_id
LEFT JOIN (SELECT DISTINCT user_id, activity_id FROM activity_record WHERE activity_id = %s) d ON d.user_id = a.id
LEFT JOIN activity f ON f.id = d.activity_id
LEFT JOIN station_cooperation s ON s.id = a.cid
LEFT JOIN system_dict_data sd1 ON sd1.`value` = s.platform COLLATE utf8mb4_0900_ai_ci
LEFT JOIN system_dict_data sd2 ON sd2.`value` = s.channel COLLATE utf8mb4_0900_ai_ci
LEFT JOIN system_dict_data sd3 ON sd3.`value` = s.scene COLLATE utf8mb4_0900_ai_ci
WHERE a.create_time >= %s AND a.create_time < %s
"""


def to_plain(v):
    """Decimal 等转成可写单元格的类型；19位雪花ID转字符串保留精度"""
    if isinstance(v, decimal.Decimal):
        if v == v.to_integral_value() and abs(v) >= 1e15:
            return str(int(v))
        return float(v)
    if isinstance(v, int) and abs(v) >= 1e15:
        return str(v)
    if isinstance(v, str):
        return ''.join(ch for ch in v if ch >= ' ' or ch in '\t\n\r')
    if isinstance(v, datetime.datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    return v


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
        # Sheet1: 回收订单
        cur.execute(SQL_ORDER, (start, end))
        h1 = [d[0] for d in cur.description]
        rows1 = cur.fetchall()
        ws1 = wb.active
        ws1.title = "回收订单"
        ws1.append(h1)
        for r in rows1:
            ws1.append([to_plain(x) for x in r])
        print(f"回收订单: {len(rows1)} 行, {len(h1)} 列")

        # Sheet2: 会员用户
        cur.execute(SQL_MEMBER, (ACTIVITY_ID, start, end))
        h2 = [d[0] for d in cur.description]
        rows2 = cur.fetchall()
        ws2 = wb.create_sheet("会员用户")
        ws2.append(h2)
        for r in rows2:
            ws2.append([to_plain(x) for x in r])
        print(f"会员用户: {len(rows2)} 行, {len(h2)} 列")
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