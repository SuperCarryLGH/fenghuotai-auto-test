import pytest
from config import APP_URL


class TestOrderGetCount:
    """获得交易订单数量"""

    @pytest.mark.smoke
    def test_OrderGetCount(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/order/get-count"
        params = {"id": autotest_order_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
