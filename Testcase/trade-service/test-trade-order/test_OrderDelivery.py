import time
import pytest
from config import ADMIN_URL


class TestOrderDelivery:
    """订单发货"""

    @pytest.mark.smoke
    def test_OrderDelivery(self, api_session, auth_headers, order_id):
        url = f"{ADMIN_URL}/admin-api/trade/order/delivery"
        body = {
            "id": order_id,
            "logisticsId": 1,
            "logisticsNo": f"SF{int(time.time())}",
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
