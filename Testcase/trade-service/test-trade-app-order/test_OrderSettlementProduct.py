import pytest
from config import APP_URL


class TestOrderSettlementProduct:
    """获得商品结算信息"""

    @pytest.mark.smoke
    def test_OrderSettlementProduct(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/order/settlement-product"
        params = {"id": autotest_order_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
