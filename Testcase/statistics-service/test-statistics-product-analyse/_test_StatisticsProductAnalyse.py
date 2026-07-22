import pytest
from config import ADMIN_URL


class TestStatisticsProductAnalyse:
    """获得商品统计分析"""

    @pytest.mark.smoke
    def test_StatisticsProductAnalyse(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/product/analyse"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
