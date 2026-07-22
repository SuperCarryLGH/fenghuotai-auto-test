import pytest
from config import ADMIN_URL


class TestOrderUpdatePrice:
    """订单调价"""

    @pytest.mark.smoke
    def test_OrderUpdatePrice(self, api_session, auth_headers, order_id):
        url = f"{ADMIN_URL}/admin-api/trade/order/update-price"
        body = {
            "id": order_id,
            "adjustPrice": -100,
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
