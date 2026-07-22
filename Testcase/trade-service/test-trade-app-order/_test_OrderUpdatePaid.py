import pytest
from config import APP_URL


class TestOrderUpdatePaid:
    """更新订单为已支付"""

    @pytest.mark.smoke
    def test_OrderUpdatePaid(self, api_session, auth_headers, autotest_order_id):
        url = f"{APP_URL}/app-api/trade/order/update-paid"
        body = {"id": autotest_order_id}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
