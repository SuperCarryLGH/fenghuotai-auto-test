import pytest
from config import APP_URL
from Common.loader import load_station_order
from Common.login import Login

station_msg = load_station_order()


class TestStationOrderSubmit:
    """单次 面对面 下单"""

    @pytest.mark.smoke
    def test_station_order_submit(self, api_session, login_tool):
        mobile = station_msg["station_msg1"]["mobile"]
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/app-api/recycle/order/station-order-submit"
        payload = {
            "platform": station_msg["station_msg1"                                                                                                                                                                                                                         ]["platform"],
            "provider": station_msg["station_msg1"]["provider"],
            #"channel": station_msg["station_msg1"]["channel"],
            "scene": station_msg["station_msg1"]["scene"],
            "lat": station_msg["station_msg1"]["lat"],
            "lon": station_msg["station_msg1"]["lon"],
            "itemId": station_msg["station_msg1"]["itemId"],
            "pics": station_msg["station_msg1"]["pics"],
            "promoterId": station_msg["station_msg1"]["promoterId"],
            "promotionPlatform": station_msg["station_msg1"]["promotionPlatform"],
            "promotionChannel": station_msg["station_msg1"]["promotionChannel"],
            "promotionStationId": station_msg["station_msg1"]["promotionStationId"],
            "activityId": station_msg["station_msg1"]["activityId"], 
            "payType": station_msg["station_msg1"]["payType"],
            "stationId": station_msg["station_msg1"]["stationId"],
            "name": station_msg["station_msg1"]["name"],
            "mobile": station_msg["station_msg1"]["mobile"],
            "predictWeight": station_msg["station_msg1"]["predictWeight"],
        }

        resp = api_session.post(url, json=payload, headers=headers)
        print(resp.text)
        assert resp.status_code == 200
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        return data
