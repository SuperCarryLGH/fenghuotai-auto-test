import pytest
from config import APP_URL
from Common.login import Login


class TestMiniOrderSubmit:
    """单次 mini 下单"""

    @pytest.mark.smoke
    def test_mini_order_submit(self, api_session, login_tool):
        token = login_tool.app_login(mobile="18338956022")
        print(token)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "web",
            "provider": "",
            "bizMode": "WeightClothes",
            "userName": "147",
            "userPhone": "18338956022",
            "addressId": "2067094249466097666",
            "appointmentDate": "2026-07-11",
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": "周五",
            "estimatedInfo": "5~10kg",
            "lat": "34.795439",
            "lon": "113.688145",
            "num": 5,
            #"activityId":12,
            "predictWeight": "5~10kg",
            #"channel":"",
            #"scene":"smk",
        }

        resp = api_session.post(url, json=payload, headers=headers)
        #assert resp.status_code == 200
        data = resp.json()
        # assert data["code"] == 0
        print(token)
        print(data)
