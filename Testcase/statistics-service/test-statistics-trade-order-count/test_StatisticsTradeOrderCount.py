import pytest
from config import ADMIN_URL


class TestStatisticsTradeOrderCount:
    """获得交易订单数量"""

    @pytest.mark.smoke
    def test_StatisticsTradeOrderCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/order-count"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
