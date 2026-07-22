import pytest
from config import ADMIN_URL


class TestOrderPickUpById:
    """订单核销"""

    @pytest.mark.smoke
    def test_OrderPickUpById(self, api_session, auth_headers, order_id):
        url = f"{ADMIN_URL}/admin-api/trade/order/pick-up-by-id"
        params = {"id": order_id}
        resp = api_session.put(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
