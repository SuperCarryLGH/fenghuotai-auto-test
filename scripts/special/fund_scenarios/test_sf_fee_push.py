"""
顺丰清单运费推送回调幂等验证

流程:
1. 下单 → 拿真实运单号 → 拍 DB 快照
2. 并发 10 次回调
3. 等 35s → 再并发 10 次回调
4. 每 5s 单次回调 1 次 × N 轮，每次查 DB
5. 最终校验

运行: TEST_ENV=dev USE_MOCK=false pytest -v -s Testcase/fund_scenarios/test_sf_fee_push.py
"""
import sys, os, time, json, hashlib, base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

import pytest
import pymysql
import requests
from config import APP_URL, DB_CONFIG
from Common.login import Login

USER_MOBILE = "15617637160"
SF_CHECKWORD = "YOUR_SF_CHECKWORD"
SF_CUSTOMER_ACCT = "5776559188"
CONCURRENT_COUNT = 10
SINGLE_ROUNDS = 5          # 单次回调轮数
SINGLE_INTERVAL = 5        # 每轮间隔秒

_BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}


def _sf_sign(content: str) -> str:
    raw = f"{content}{SF_CHECKWORD}".encode()
    return base64.b64encode(hashlib.md5(raw).digest()).decode()


def _query_order(order_no: str) -> dict:
    conn = pymysql.connect(
        host=DB_CONFIG["host"], port=DB_CONFIG["port"],
        user=DB_CONFIG["user"], password=DB_CONFIG["password"],
        database=DB_CONFIG["database"], connect_timeout=3,
    )
    c = conn.cursor()
    c.execute("SELECT total_price, pay_price, express_order FROM recycle_order WHERE order_no = %s", (order_no,))
    row = c.fetchone()
    c.close()
    conn.close()
    if row:
        return {"total_price": row[0] or 0, "pay_price": row[1] or 0, "express_order": row[2] or ""}
    return {}


def _post_callback(data: dict) -> dict:
    try:
        resp = requests.post(f"{APP_URL}/app-api/recycle/express/fee-push/sf", data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded", **_BASE_HEADERS,
        }, timeout=30)
        return {"status": resp.status_code, "body": resp.json() if resp.status_code == 200 else resp.text[:200]}
    except Exception as e:
        return {"status": -1, "body": str(e)}


class TestSfFeePush:
    """顺丰回调幂等验证"""

    @pytest.mark.slow
    def test_sf_fee_push(self, api_session):
        print("=" * 60)
        print("顺丰回调幂等验证")
        print("=" * 60)

        login = Login(session=api_session)
        user_token = login.app_login_with(mobile=USER_MOBILE, code="9999")
        user_h = {**_BASE_HEADERS, **Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {user_token}"}

        # ── 下单 ──
        print("\n[1] 创建订单...")
        resp = requests.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", json={
            "platform": "web", "provider": "", "bizMode": "WeightClothes",
            "userName": "郑豪", "userPhone": USER_MOBILE,
            "addressId": "2071903351920783362",
            "appointmentDate": "2026-07-10", "appointmentTimePeriod": "10:00-11:00",
            "appointmentWeekStr": "周五",
            "estimatedInfo": "5~10kg", "lat": "34.79678190031236", "lon": "113.68181482834622",
            "num": 5, "predictWeight": "5~10kg",
        }, headers=user_h, timeout=30)
        r = resp.json()
        order_no = (r.get("data") or {}).get("orderNo", "")
        print(f"    orderNo={order_no}")
        if not order_no: return

        info = _query_order(order_no)
        waybill_no = info.get("express_order", "")
        if not waybill_no:
            print("    ❌ 未查到运单号"); return
        total_before = info["total_price"]
        pay_before = info["pay_price"]
        print(f"    waybillNo={waybill_no} | total_price={total_before} pay_price={pay_before}")

        # ── 构造回调 ──
        print(f"\n[2] 构造回调...")
        fee_data = {
            "orderNo": order_no, "quantity": 1.0, "meterageWeightQty": 6.9,
            "customerAcctCode": SF_CUSTOMER_ACCT,
            "feeList": [{
                "feeTypeCode": "1", "settlementTypeCode": "2",
                "inputTm": int(time.time() * 1000), "feeName": "运费",
                "versionNo": 0, "paymentTypeCode": "3",
                "customerAcctCode": SF_CUSTOMER_ACCT,
                "feeAmtInd": 24.0, "currencyCode": "CNY",
                "feeIndType": 0, "feeAmt": 24.0, "waybillNo": waybill_no,
            }],
            "productName": "顺丰干配", "waybillNo": waybill_no,
        }
        content_str = json.dumps(fee_data, ensure_ascii=False)
        data = {"content": content_str}
        if SF_CHECKWORD != "YOUR_SF_CHECKWORD":
            data["sign"] = _sf_sign(content_str)
        time.sleep(1)
        # ── 第一次并发 ──
        print(f"\n[3] 第一次并发 {CONCURRENT_COUNT} 次回调...")
        start = time.time()
        with ThreadPoolExecutor(max_workers=CONCURRENT_COUNT) as pool:
            futures = {pool.submit(_post_callback, data): i for i in range(CONCURRENT_COUNT)}
            for f in as_completed(futures):
                idx = futures[f]
                r = f.result()
                icon = "✅" if r["status"] == 200 else "❌"
                print(f"    并发#{idx+1:02d}: {icon} status={r['status']} {r['body']}")
        print(f"    耗时 {time.time()-start:.1f}s")
        s1 = _query_order(order_no)
        print(f"    [DB] total_price={s1['total_price']} pay_price={s1['pay_price']}")

        # ── 等 35s 再并发 ──
        print(f"\n[4] 等待 35s ...")
        for i in range(35, 0, -5):
            print(f"    {i}s ...")
            time.sleep(5)

        print(f"\n[5] 第二次并发 {CONCURRENT_COUNT} 次回调...")
        start = time.time()
        with ThreadPoolExecutor(max_workers=CONCURRENT_COUNT) as pool:
            futures = {pool.submit(_post_callback, data): i for i in range(CONCURRENT_COUNT)}
            for f in as_completed(futures):
                idx = futures[f]
                r = f.result()
                icon = "✅" if r["status"] == 200 else "❌"
                print(f"    并发#{idx+1:02d}: {icon} status={r['status']} {r['body']}")
        print(f"    耗时 {time.time()-start:.1f}s")
        s2 = _query_order(order_no)
        print(f"    [DB] total_price={s2['total_price']} pay_price={s2['pay_price']}")

        # ── 每 5s 单次回调 ──
        print(f"\n[6] 每 {SINGLE_INTERVAL}s 单次回调 × {SINGLE_ROUNDS} 轮...")
        for round_idx in range(1, SINGLE_ROUNDS + 1):
            print(f"\n  --- 第 {round_idx}/{SINGLE_ROUNDS} 轮 ---")
            r = _post_callback(data)
            icon = "✅" if r["status"] == 200 else "❌"
            print(f"    单次: {icon} status={r['status']} {r['body']}")
            s = _query_order(order_no)
            print(f"    [DB] total_price={s['total_price']} pay_price={s['pay_price']}")
            if round_idx < SINGLE_ROUNDS:
                time.sleep(SINGLE_INTERVAL)

        # ── 最终校验 ──
        final = _query_order(order_no)
        print(f"\n[7] 最终校验...")
        print(f"    初始:   total_price={total_before} pay_price={pay_before}")
        print(f"    一次并发后: total_price={s1['total_price']} pay_price={s1['pay_price']}")
        print(f"    二次并发后: total_price={s2['total_price']} pay_price={s2['pay_price']}")
        print(f"    最终:   total_price={final['total_price']} pay_price={final['pay_price']}")

        delta = final['total_price'] - total_before
        if delta == 0:
            print("    ⚠️ 金额完全未变 (回调可能未触发结算)")
        elif abs(delta) == 24.0:
            print("    ✅ 金额只增加了24元 (运费) — 幂等有效")
        else:
            print(f"    ❌ 金额变了 {delta} — 幂等可能失效")

        print("\n" + "=" * 60)
        print("幂等验证完毕")
        print("=" * 60)
