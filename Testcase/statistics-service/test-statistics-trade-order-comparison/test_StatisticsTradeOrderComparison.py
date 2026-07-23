import pytest
from config import ADMIN_URL


class TestStatisticsTradeOrderComparison:
    """获得交易订单数量"""

    @pytest.mark.smoke
    def test_StatisticsTradeOrderComparison(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/order-comparison"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
