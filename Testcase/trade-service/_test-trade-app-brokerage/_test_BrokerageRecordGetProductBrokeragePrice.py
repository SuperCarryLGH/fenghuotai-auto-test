import pytest
from config import APP_URL


class TestBrokerageRecordGetProductBrokeragePrice:
    """获得商品的分销金额"""

    @pytest.mark.smoke
    def test_BrokerageRecordGetProductBrokeragePrice(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-record/get-product-brokerage-price"
        params = {"id": "trade_app_brokerage_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
