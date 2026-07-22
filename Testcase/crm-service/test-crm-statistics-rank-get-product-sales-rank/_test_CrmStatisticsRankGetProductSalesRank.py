import pytest
from config import ADMIN_URL


class TestCrmStatisticsRankGetProductSalesRank:
    """获得产品销量排行榜"""

    @pytest.mark.smoke
    def test_CrmStatisticsRankGetProductSalesRank(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-rank/get-product-sales-rank"
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
