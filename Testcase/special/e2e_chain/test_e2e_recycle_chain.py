"""
C端回收全链路 E2E 测试
用户扫码 → 站点面对面接单 → 称重 → 结算 → 完成
"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login


def login_as(api_session, mobile):
    headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000))}
    resp = api_session.post(
        f"{ADMIN_URL}/admin-api/system/auth/sms-login",
        json={"mobile": mobile, "code": "9999"}, headers=headers,
    )
    assert resp.status_code == 200 and resp.json()["code"] == 0
    return {"Authorization": f"Bearer {resp.json()['data']['accessToken']}"}


class TestE2ERecycleChain:
    """扫码面对面回收全链路"""

    @pytest.mark.smoke
    def test_e2e_recycle(self, api_session):
        station_headers = login_as(api_session, "18600000000")

        # ──────────────────────────────────────────
        # Step 1: 站点老板扫码接单
        # ──────────────────────────────────────────
        print("\n[Step 1] 用户扫码 → 站点老板接单...")
        order_no = f"AUTO_{int(time.time())}"
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/order/station-order-submit",
            json={
                "userPhone": "15617637160",
                "orderNo": order_no,
                "verifyCode": "9999",
            },
            headers=station_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        order_id = resp.json()["data"].get("id") or resp.json()["data"]
        print(f"  ✅ 接单成功 order_id={order_id}")

        # ──────────────────────────────────────────
        # Step 2: 称重
        # ──────────────────────────────────────────
        print("\n[Step 2] 称重...")
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/order/order-weighting",
            json={"orderId": order_id, "weight": 5000},
            headers=station_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 称重完成 5000g")

        # ──────────────────────────────────────────
        # Step 3: 结算（钱包）
        # ──────────────────────────────────────────
        print("\n[Step 3] 钱包结算...")
        resp = api_session.post(
            f"{APP_URL}/app-api/recycle/order/pay-order",
            json={"orderId": order_id, "payType": 1},
            headers=station_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 结算完成")

        # ──────────────────────────────────────────
        # Step 4: 确认订单状态
        # ──────────────────────────────────────────
        print("\n[Step 4] 确认订单完成...")
        resp = api_session.get(
            f"{APP_URL}/app-api/recycle/order/getOrderInfo",
            params={"orderId": order_id},
            headers=station_headers,
        )
        assert resp.status_code == 200 and resp.json()["code"] == 0
        print(f"  ✅ 订单状态={resp.json()['data'].get('status')}")

        print(f"\n🎉 面对面回收全链路通过! order_id={order_id}")
