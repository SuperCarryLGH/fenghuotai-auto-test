import pytest
from config import APP_URL


class TestOrderGetDetail:
    """获得交易订单"""

    @pytest.mark.smoke
    def test_OrderGetDetail(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/order/get-detail"
        params = {"id": "trade_app_order_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
