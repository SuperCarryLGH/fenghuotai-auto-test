import pytest
from config import ADMIN_URL


class TestStatisticsTradeList:
    """获得交易状况明细"""

    @pytest.mark.smoke
    def test_StatisticsTradeList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
