import pytest
from config import ADMIN_URL


class TestDeliveryExpressGet:
    """获得快递公司"""

    @pytest.mark.smoke
    def test_DeliveryExpressGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/delivery/express/get"
        params = {"id": "trade_delivery_express_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
