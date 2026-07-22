"""
S5 清运结算 — 自动化链路

流程: 下单 → 站点接单 → 称重 → 支付 → 呼叫清运 → 司机接单 → 到达 → 称重 → 称重完成 → 触发清运结算

运行: TEST_ENV=dev USE_MOCK=false pytest -v -s Testcase/fund_scenarios/test_clear_settle.py
"""
import sys, os, time
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

import pytest
import requests
from config import ADMIN_URL, APP_URL
from Common.login import Login

STATION_ID = 1
STATION_MOBILE = "18600000000"
DRIVER_MOBILE = "18600000001"
USER_MOBILE = "15617637160"
SORTING_CENTER_ID = 2074701657159761922

_BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}


def _api_post(url: str, payload: dict, headers: dict) -> dict:
    print(f"    POST {url}")
    print(f"    payload={payload}")
    try:
        resp = requests.post(url, json=payload, headers={**_BASE_HEADERS, **headers}, timeout=30)
        print(f"    status={resp.status_code}, body={resp.text[:500]}")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return {"code": -1, "msg": str(e), "data": None}


def _api_get(url: str, params: dict, headers: dict) -> dict:
    print(f"    GET {url}")
    print(f"    params={params}")
    try:
        resp = requests.get(url, params=params, headers={**_BASE_HEADERS, **headers}, timeout=30)
        print(f"    status={resp.status_code}, body={resp.text[:500]}")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return {"code": -1, "msg": str(e), "data": None}


class TestClearSettle:
    """清运结算自动化"""

    @pytest.mark.slow
    def test_clear_settle(self, api_session):
        print("=" * 60)
        print("S5 清运结算 全链路自动化")
        print("=" * 60)

        login = Login(session=api_session)

        # ── 各角色 token ──
        user_token = login.app_login_with(mobile=USER_MOBILE, code="9999")
        user_h = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {user_token}"}

        station_token = login.app_login_with(mobile=STATION_MOBILE, code="9999")
        station_h = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {station_token}"}

        driver_token = login.app_login_with(mobile=DRIVER_MOBILE, code="9999")
        driver_h = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {driver_token}"}

        # ================================================================
        # Step 1: 用户下单
        # ================================================================
        print("\n[1/8] 用户下单...")
        r = _api_post(f"{APP_URL}/app-api/recycle/order/station-order-submit", {
            "platform": "web", "provider": "", "scene": "",
            "lat": 23.129163, "lon": 113.264435,
            "itemId": "", "pics": "", "promoterId": "",
            "promotionPlatform": "", "promotionChannel": "", "promotionStationId": "",
            "activityId": "", "payType": 2,
            "stationId": STATION_ID, "name": "站点1", "mobile": USER_MOBILE,
            "predictWeight": 50000025,
        }, user_h)
        order_data = (r.get("data") or {})
        order_id = int(order_data.get("id", 0))
        print(f"    orderId={order_id}")
        if not order_id:
            print("    ❌ 下单失败, 终止")
            return
        time.sleep(1)

        # ================================================================
        # Step 2: 站点接单 → station token
        # ================================================================
        print("\n[2/8] 站点接单...")
        r = _api_post(f"{ADMIN_URL}/admin-api/recycle/app-order/receive", {
            "orderId": order_id, "status": 21, "payType": 2, "payPrice": 12.5,
            "phoneTailFour": "7160",
        }, station_h)
        time.sleep(1)

        # ================================================================
        # Step 3: 称重 + 支付 → station token
        # ================================================================
        print("\n[3/8] 查品类...")
        r = _api_get(f"{ADMIN_URL}/admin-api/recycle/app-order/get-order-info", {"id": order_id}, station_h)
        order_detail = (r.get("data") or {}) if r.get("code") == 0 else {}
        items = order_detail.get("items") or order_detail.get("recycleOrderItemList") or []
        item_id = int(items[0].get("id") or items[0].get("recycleOrderItemId", 0)) if items else 0
        print(f"    recycleOrderItemId={item_id}")

        print("\n[3/8] 称重...")
        _api_post(f"{ADMIN_URL}/admin-api/recycle/app-order/order-weighting", {
            "orderId": order_id, "recycleOrderItemId": item_id,
            "price": 2.5, "weight": 5,
        }, station_h)
        time.sleep(1)

        print("\n[3/8] 支付...")
        _api_post(f"{ADMIN_URL}/admin-api/recycle/app-order/pay-order", {
            "orderId": order_id, "payPrice": 100, "payType": 2,
        }, station_h)
        time.sleep(2)

        # ================================================================
        # Step 4: 呼叫清运 → station token
        # ================================================================
        print("\n[4/8] 呼叫清运...")
        r = _api_post(f"{ADMIN_URL}/admin-api/recycle/app-order/call-clean-now", {
            "stationId": STATION_ID, "warehouseId": 0,
            "operationCenterId": SORTING_CENTER_ID,
            "appointmentDate": "2026-07-10", "appointmentTimePeriod": "10:00-11:00",
            "appointmentWeekStr": "周五", "clearType": 1, "clearTarget": 2,
        }, station_h)
        clear_data = (r.get("data") or {}) if r.get("code") == 0 else {}
        clear_order_id = int(clear_data.get("id", 0))
        print(f"    clearOrderId={clear_order_id}")
        if not clear_order_id:
            print(f"    ❌ 呼叫清运失败: {r.get('msg')}")
            return
        time.sleep(1)

        # ================================================================
        # Step 5-8: 司机流程 → driver token
        # ================================================================

        print("\n[5/8] 司机接单...")
        _api_post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/accept", {
            "id": clear_order_id,
        }, driver_h)
        time.sleep(1)

        print("\n[6/8] 司机到达...")
        _api_post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/arrive", {
            "id": clear_order_id,
        }, driver_h)
        time.sleep(1)

        print("\n[7/8] 司机称重...")
        _api_post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/update-weight", {
            "clearOrderId": clear_order_id, "packageNo": "CL001",
            "itemId": 2001, "weight": 100,
        }, driver_h)
        time.sleep(1)

        print("\n[8/8] 司机称重完成 → 触发清运结算...")
        _api_post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/weighing-complete", {
            "id": clear_order_id,
        }, driver_h)
        time.sleep(3)

        print("\n" + "=" * 60)
        print("清运结算链路执行完毕")
        print("=" * 60)
