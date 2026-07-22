import json
import os
import time
import pytest
from config import APP_URL
from Common.login import Login

ORDER_FILE = os.path.join(os.path.dirname(__file__), "last_order.json")


class TestMiniOrderSubmit:
    """单次 mini 下单 — 登录走 Login 类，自动跟随 USE_REAL_SMS_CODE 开关"""

    @pytest.mark.smoke
    def test_mini_order_submit(self, api_session, login_tool):
        mobile = "15617637160"

        token = login_tool.app_login_with(mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        print(f"  ✅ 登录成功")

        print(f"[Step 3] 下单...")
        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "web",
            "provider": "",
            "bizMode": "WeightClothes",
            "userName": "QA",
            "userPhone": mobile,
            "addressId": "2079049311432077313",
            "appointmentDate": time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400)),
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": "周三",
            "estimatedInfo": "5~10kg",
            "lat": "34.79678190031236",
            "lon": "113.68181482834622",
            "num": 5,
            "predictWeight": "5~10kg",
        }

        resp = api_session.post(url, json=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        order_id = data["data"]["id"]
        print(f"  ✅ 下单成功: order_id={order_id}")

        with open(ORDER_FILE, "w") as f:
            json.dump({"orderId": order_id, "userPhone": mobile}, f)
        print(f"已保存至 {ORDER_FILE}")
