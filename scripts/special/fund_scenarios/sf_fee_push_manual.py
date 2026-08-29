"""
顺丰费用回调手动触发工具

使用方式:
  # 查询订单信息
  python sf_fee_push_manual.py query <order_no>

  # 单次回调（默认运费24元）
  python sf_fee_push_manual.py push <order_no>

  # 单次回调（指定金额）
  python sf_fee_push_manual.py push <order_no> --amount 30

  # 幂等测试（并发+多轮）
  python sf_fee_push_manual.py test <order_no>

  # 幂等测试（指定并发数和轮数）
  python sf_fee_push_manual.py test <order_no> --concurrent 5 --rounds 3
"""
import sys
import os
import time
import json
import hashlib
import base64
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

import pymysql
import requests
from config import APP_URL, DB_CONFIG

# ============================================================
# 配置
# ============================================================
SF_CHECKWORD = "YOUR_SF_CHECKWORD"
SF_CUSTOMER_ACCT = "5776559188"

_BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}


# ============================================================
# 工具函数
# ============================================================
def _sf_sign(content: str) -> str:
    """顺丰回调签名"""
    raw = f"{content}{SF_CHECKWORD}".encode()
    return base64.b64encode(hashlib.md5(raw).digest()).decode()


def _query_order(order_no: str) -> dict:
    """查询订单信息"""
    conn = pymysql.connect(
        host=DB_CONFIG["host"], port=DB_CONFIG["port"],
        user=DB_CONFIG["user"], password=DB_CONFIG["password"],
        database=DB_CONFIG["database"], connect_timeout=3,
    )
    c = conn.cursor()
    c.execute(
        "SELECT total_price, pay_price, express_order, status, sub_status "
        "FROM recycle_order WHERE order_no = %s",
        (order_no,),
    )
    row = c.fetchone()
    c.close()
    conn.close()
    if row:
        return {
            "total_price": row[0] or 0,
            "pay_price": row[1] or 0,
            "express_order": row[2] or "",
            "status": row[3],
            "sub_status": row[4],
        }
    return {}


def _build_callback_data(order_no: str, waybill_no: str, fee_amt: float = 24.0) -> dict:
    """构造顺丰回调数据"""
    fee_data = {
        "orderNo": order_no,
        "quantity": 1.0,
        "meterageWeightQty": 6.9,
        "customerAcctCode": SF_CUSTOMER_ACCT,
        "feeList": [{
            "feeTypeCode": "1",
            "settlementTypeCode": "2",
            "inputTm": int(time.time() * 1000),
            "feeName": "运费",
            "versionNo": 0,
            "paymentTypeCode": "3",
            "customerAcctCode": SF_CUSTOMER_ACCT,
            "feeAmtInd": fee_amt,
            "currencyCode": "CNY",
            "feeIndType": 0,
            "feeAmt": fee_amt,
            "waybillNo": waybill_no,
        }],
        "productName": "顺丰干配",
        "waybillNo": waybill_no,
    }
    content_str = json.dumps(fee_data, ensure_ascii=False)
    data = {"content": content_str}
    if SF_CHECKWORD != "YOUR_SF_CHECKWORD":
        data["sign"] = _sf_sign(content_str)
    return data


def _post_callback(data: dict) -> dict:
    """发送回调请求"""
    try:
        resp = requests.post(
            f"{APP_URL}/app-api/recycle/express/fee-push/sf",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded", **_BASE_HEADERS},
            timeout=30,
        )
        return {
            "status": resp.status_code,
            "body": resp.json() if resp.status_code == 200 else resp.text[:200],
        }
    except Exception as e:
        return {"status": -1, "body": str(e)}


# ============================================================
# 命令: query - 查询订单信息
# ============================================================
def cmd_query(order_no: str):
    """查询订单信息"""
    print(f"查询订单: {order_no}")
    info = _query_order(order_no)
    if not info:
        print("  ❌ 订单不存在")
        return

    print(f"  运单号: {info['express_order']}")
    print(f"  总金额: {info['total_price']}")
    print(f"  实付金额: {info['pay_price']}")
    print(f"  状态: {info['status']}")
    print(f"  子状态: {info['sub_status']}")


# ============================================================
# 命令: push - 单次回调
# ============================================================
def cmd_push(order_no: str, fee_amt: float = 24.0):
    """单次回调"""
    print(f"订单: {order_no}")
    print(f"回调金额: {fee_amt} 元")

    # 查询订单
    info = _query_order(order_no)
    if not info:
        print("  ❌ 订单不存在")
        return

    waybill_no = info.get("express_order", "")
    if not waybill_no:
        print("  ❌ 未查到运单号")
        return

    print(f"  运单号: {waybill_no}")
    print(f"  回调前金额: total_price={info['total_price']}, pay_price={info['pay_price']}")

    # 构造并发送回调
    data = _build_callback_data(order_no, waybill_no, fee_amt)
    print(f"\n发送回调...")
    result = _post_callback(data)
    icon = "✅" if result["status"] == 200 else "❌"
    print(f"  {icon} status={result['status']}")
    print(f"  响应: {result['body']}")

    # 查询回调后金额
    time.sleep(1)
    info_after = _query_order(order_no)
    print(f"\n  回调后金额: total_price={info_after['total_price']}, pay_price={info_after['pay_price']}")

    delta = info_after["total_price"] - info["total_price"]
    if delta == 0:
        print(f"  ⚠️ 金额未变化")
    elif abs(delta) == fee_amt:
        print(f"  ✅ 金额增加了 {fee_amt} 元")
    else:
        print(f"  ❌ 金额变化异常: {delta}")


# ============================================================
# 命令: test - 幂等测试
# ============================================================
def cmd_test(order_no: str, concurrent: int = 10, rounds: int = 5, interval: int = 5):
    """幂等测试"""
    print("=" * 60)
    print(f"顺丰回调幂等验证 - 订单: {order_no}")
    print(f"并发数: {concurrent}, 轮数: {rounds}, 间隔: {interval}s")
    print("=" * 60)

    # 查询订单
    info = _query_order(order_no)
    if not info:
        print("❌ 订单不存在")
        return

    waybill_no = info.get("express_order", "")
    if not waybill_no:
        print("❌ 未查到运单号")
        return

    total_before = info["total_price"]
    pay_before = info["pay_price"]
    print(f"\n运单号: {waybill_no}")
    print(f"初始: total_price={total_before}, pay_price={pay_before}")

    # 构造回调数据
    data = _build_callback_data(order_no, waybill_no)
    time.sleep(1)

    # 第一次并发
    print(f"\n[1] 第一次并发 {concurrent} 次回调...")
    start = time.time()
    with ThreadPoolExecutor(max_workers=concurrent) as pool:
        futures = {pool.submit(_post_callback, data): i for i in range(concurrent)}
        for f in as_completed(futures):
            idx = futures[f]
            r = f.result()
            icon = "✅" if r["status"] == 200 else "❌"
            print(f"    并发#{idx + 1:02d}: {icon} status={r['status']} {r['body']}")
    print(f"    耗时 {time.time() - start:.1f}s")
    s1 = _query_order(order_no)
    print(f"    [DB] total_price={s1['total_price']}, pay_price={s1['pay_price']}")

    # 等待 35s
    print(f"\n[2] 等待 35s ...")
    for i in range(35, 0, -5):
        print(f"    {i}s ...")
        time.sleep(5)

    # 第二次并发
    print(f"\n[3] 第二次并发 {concurrent} 次回调...")
    start = time.time()
    with ThreadPoolExecutor(max_workers=concurrent) as pool:
        futures = {pool.submit(_post_callback, data): i for i in range(concurrent)}
        for f in as_completed(futures):
            idx = futures[f]
            r = f.result()
            icon = "✅" if r["status"] == 200 else "❌"
            print(f"    并发#{idx + 1:02d}: {icon} status={r['status']} {r['body']}")
    print(f"    耗时 {time.time() - start:.1f}s")
    s2 = _query_order(order_no)
    print(f"    [DB] total_price={s2['total_price']}, pay_price={s2['pay_price']}")

    # 单次回调
    print(f"\n[4] 每 {interval}s 单次回调 × {rounds} 轮...")
    for round_idx in range(1, rounds + 1):
        print(f"\n  --- 第 {round_idx}/{rounds} 轮 ---")
        r = _post_callback(data)
        icon = "✅" if r["status"] == 200 else "❌"
        print(f"    单次: {icon} status={r['status']} {r['body']}")
        s = _query_order(order_no)
        print(f"    [DB] total_price={s['total_price']}, pay_price={s['pay_price']}")
        if round_idx < rounds:
            time.sleep(interval)

    # 最终校验
    final = _query_order(order_no)
    print(f"\n[5] 最终校验...")
    print(f"    初始:     total_price={total_before}, pay_price={pay_before}")
    print(f"    一次并发后: total_price={s1['total_price']}, pay_price={s1['pay_price']}")
    print(f"    二次并发后: total_price={s2['total_price']}, pay_price={s2['pay_price']}")
    print(f"    最终:     total_price={final['total_price']}, pay_price={final['pay_price']}")

    delta = final["total_price"] - total_before
    if delta == 0:
        print("    ⚠️ 金额完全未变 (回调可能未触发结算)")
    elif abs(delta) == 24.0:
        print("    ✅ 金额只增加了24元 (运费) — 幂等有效")
    else:
        print(f"    ❌ 金额变了 {delta} — 幂等可能失效")

    print("\n" + "=" * 60)
    print("幂等验证完毕")
    print("=" * 60)


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="顺丰费用回调手动触发工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # query 命令
    p_query = subparsers.add_parser("query", help="查询订单信息")
    p_query.add_argument("order_no", help="订单号")

    # push 命令
    p_push = subparsers.add_parser("push", help="单次回调")
    p_push.add_argument("order_no", help="订单号")
    p_push.add_argument("--amount", type=float, default=24.0, help="回调金额(元), 默认24")

    # test 命令
    p_test = subparsers.add_parser("test", help="幂等测试")
    p_test.add_argument("order_no", help="订单号")
    p_test.add_argument("--concurrent", type=int, default=10, help="并发数, 默认10")
    p_test.add_argument("--rounds", type=int, default=5, help="单次回调轮数, 默认5")
    p_test.add_argument("--interval", type=int, default=5, help="轮次间隔秒数, 默认5")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "query":
        cmd_query(args.order_no)
    elif args.command == "push":
        cmd_push(args.order_no, args.amount)
    elif args.command == "test":
        cmd_test(args.order_no, args.concurrent, args.rounds, args.interval)


if __name__ == "__main__":
    main()
