import pytest
from config import APP_URL


class TestDeliveryExpressList:
    """获得快递公司列表"""

    @pytest.mark.smoke
    def test_DeliveryExpressList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/delivery/express/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
