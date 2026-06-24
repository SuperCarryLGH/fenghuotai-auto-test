import pytest
from config import APP_URL
from Common.login import Login


class TestMiniOrderSubmit:
    """单次 mini 下单"""

    @pytest.mark.smoke
    def test_mini_order_submit(self, api_session, login_tool):
        mobile = "15617617160"
        token = login_tool.app_login(mobile=mobile)
        print(token)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "web",
            "provider": "",
            "channel": "",
            "scene": "",
            # "lat": ,
            # "lon": ,
            "itemId": "",
            "pics": "",
            "promoterId": "",
            "promotionPlatform": "",
            "promotionChannel": "",
            "promotionStationId": "",
            "activityId": "13",
            #"payType": 1,
            "appointmentDate": "2026-06-18",
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": "周四",
            "estimatedInfo": "",
            "predictWeight": "",
            "addressId": "2066773491032387585",
        }

        resp = api_session.post(url, json=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        # assert data["code"] == 0
        print(token)
        print(data)
