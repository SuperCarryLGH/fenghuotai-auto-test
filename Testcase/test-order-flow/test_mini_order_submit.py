import pytest
from config import APP_URL


class TestMiniOrderSubmit:
    """单次 mini 下单"""

    @pytest.mark.smoke
    def test_mini_order_submit(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit"
        payload = {
            "platform": "微信小程序",
            "provider": "",
            "channel": "",
            "scene": "",
            "lat": 34.789,
            "lon": 113.665,
            "itemId": 1001,
            "pics": "",
            "promoterId": "",
            "promotionPlatform": "",
            "promotionChannel": "",
            "promotionStationId": "",
            "activityId": "",
            "payType": 1,
            "appointmentDate": "2026-06-10",
            "appointmentTimePeriod": "上午",
            "appointmentWeekStr": "周三",
            "estimatedInfo": "",
            "predictWeight": "5.0",
            "addressId": "ADDR_001",
        }

        resp = api_session.post(url, json=payload, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
