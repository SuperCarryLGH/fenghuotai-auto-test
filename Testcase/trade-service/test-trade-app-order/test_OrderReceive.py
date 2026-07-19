import pytest
from config import APP_URL


class TestOrderReceive:
    """确认交易订单收货"""

    @pytest.mark.smoke
    def test_OrderReceive(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/order/receive"
        body = {"id": autotest_order_id}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
