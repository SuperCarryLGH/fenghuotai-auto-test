import pytest
from datetime import date, timedelta
from config import APP_URL
from Common.login import Login

_WEEKDAY_MAP = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}


class TestMiniOrderSubmit:
    """单次 mini 下单"""

    @pytest.mark.smoke
    def test_mini_order_submit(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15204643417")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        tomorrow = date.today() + timedelta(days=1)
        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "web",
            "provider": "",
            "bizMode": "WeightClothes",
            "userName": "测试0730",
            "userPhone": "15204643417",
            "addressId": "2085525396974993422",
            "appointmentDate": tomorrow.strftime("%Y-%m-%d"),
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": _WEEKDAY_MAP[tomorrow.weekday()],
            "estimatedInfo": "5~10kg",
            "lat": "34.795439",
            "lon": "113.688145",
            "num": 5,
            "predictWeight": "5~10kg",
        }

        r = ok(api_session.post(url, json=payload, headers=headers))
        print(r)
