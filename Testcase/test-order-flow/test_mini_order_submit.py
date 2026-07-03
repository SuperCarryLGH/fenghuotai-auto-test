import pytest
from config import APP_URL
from Common.login import Login


class TestMiniOrderSubmit:
    """单次 mini 下单"""

    @pytest.mark.smoke
    def test_mini_order_submit(self, api_session, login_tool):
        token = login_tool.app_login(mobile="15617617160")
        print(token)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "web",
            "provider": "smk",
            "bizMode": "WeightClothes",
            "userName": "用户04",
            "userPhone": "15617617160",
            "addressId": "2071903932806721538",
            "appointmentDate": "2026-07-03",
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": "周五",
            "estimatedInfo": "5~10kg",
            "lat": "34.79678190031236",
            "lon": "113.68181482834622",
            "num": 5,
            #"activityId":12,
            "predictWeight": "5~10kg",
            "channel":"smk",
            "scene":"smk",
        }

        resp = api_session.post(url, json=payload, headers=headers)
        #assert resp.status_code == 200
        data = resp.json()
        # assert data["code"] == 0
        print(token)
        print(data)
