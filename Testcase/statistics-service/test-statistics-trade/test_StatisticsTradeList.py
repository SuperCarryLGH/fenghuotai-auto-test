import pytest
from config import ADMIN_URL


class TestStatisticsTradeList:
    """获得交易状况明细"""

    @pytest.mark.smoke
    def test_StatisticsTradeList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
