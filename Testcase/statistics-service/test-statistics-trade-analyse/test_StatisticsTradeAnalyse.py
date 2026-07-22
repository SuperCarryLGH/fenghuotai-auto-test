import pytest
from config import ADMIN_URL


class TestStatisticsTradeAnalyse:
    """获得交易状况统计"""

    @pytest.mark.smoke
    def test_StatisticsTradeAnalyse(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/analyse"
        params = {
            "pageNo": 1,
            "pageSize": 10,
            "beginDate": "2024-01-01",
            "endDate": "2024-12-31",
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
