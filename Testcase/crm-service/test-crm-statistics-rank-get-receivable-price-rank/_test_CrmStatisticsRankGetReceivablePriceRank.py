import pytest
from config import ADMIN_URL


class TestCrmStatisticsRankGetReceivablePriceRank:
    """获得回款金额排行榜"""

    @pytest.mark.smoke
    def test_CrmStatisticsRankGetReceivablePriceRank(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-rank/get-receivable-price-rank"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
