import pytest
from config import APP_URL


class TestOrderItemGet:
    """获得交易订单项"""

    @pytest.mark.smoke
    def test_OrderItemGet(self, api_session, auth_headers, autotest_order_id):
        url = f"{APP_URL}/app-api/trade/order/item/get"
        params = {"id": autotest_order_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
