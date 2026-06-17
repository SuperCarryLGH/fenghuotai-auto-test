import pytest
from config import APP_URL
from Common.login import Login

class TestMiniOrderSubmit:
    """单次 mini 下单"""

@pytest.mark.smoke
def test_mini_order_submit(self, api_session, login_tool):
    mobile = "19022391628"
    token = login_tool.app_login(mobile=mobile)
    headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    url = f"{APP_URL}/app-api/recycle/order/mini-order-submit"
    payload = {
        "platform": "微信小程序",
        "provider": "",
        "channel": "",
        "scene": "",
        # "lat": ,
        # "lon": ,
        "itemId": 1001,
        "pics": "",
        "promoterId": "",
        "promotionPlatform": "",
        "promotionChannel": "",
        "promotionStationId": "",
        "activityId": "12",
        # "payType": 1,
        "appointmentDate": "2026-06-17",
        "appointmentTimePeriod": "17:00-18:00",
        "appointmentWeekStr": "周三",
        "estimatedInfo": "",
        "predictWeight": "10.0",
        "addressId": "2060279024028872706",
    }

    resp = api_session.post(url, json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    # assert data["code"] == 0
    print(data)