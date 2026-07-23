import pytest
from config import ADMIN_URL


class TestOrderUpdatePrice:
    """订单调价"""

    @pytest.mark.smoke
    def test_OrderUpdatePrice(self, api_session, auth_headers, order_id, ok):
        url = f"{ADMIN_URL}/admin-api/trade/order/update-price"
        body = {
            "id": order_id,
            "adjustPrice": -100,
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
