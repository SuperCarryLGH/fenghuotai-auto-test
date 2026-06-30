from datetime import date, timedelta
import random
import pytest
from config import APP_URL
from Common.loader import load_yaml
from Common.login import Login

orders = load_yaml("batch_orders.yaml")["batch_orders"]

_WEEKDAY_MAP = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}


class TestBatchOrders:
    """批量下单 — 每单用对应手机号登录后下发"""

    @pytest.mark.smoke
    @pytest.mark.parametrize("order", orders, ids=[o["desc"] for o in orders])
    def test_batch_order(self, api_session, login_tool, order):
        mobile = order["mobile"]
        _batch_users = load_yaml("batch_users.yaml")["batch_users"]
        _mobile_to_user = {u["mobile"]: u for u in _batch_users}
        user = _mobile_to_user[mobile]
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        print(token)
        tomorrow = date.today() + timedelta(days=1)
        appointment_date = tomorrow.strftime("%Y-%m-%d")
        appointment_week_str = _WEEKDAY_MAP[tomorrow.weekday()]

        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "web",
            "provider": order["provider"],
            "channel": "",
            "scene": "",
            "pics": "",
            "promoterId": "",
            "promotionPlatform": "",
            "promotionChannel": "",
            "promotionStationId": "",
            "activityId": str(random.randint(12, 13)),
            "appointmentDate": appointment_date,
            "appointmentTimePeriod": order["appointmentTimePeriod"],
            "appointmentWeekStr": appointment_week_str,
            "estimatedInfo": "",
            "predictWeight": "",
            "addressId": user["address"]["addressId"],
            "lat": order.get("lat", ""),
            "lon": order.get("lon", ""),
        }
        print("请求:",payload)
        resp = api_session.post(url, json=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        print("响应:",data)
        assert data["code"] == 0
