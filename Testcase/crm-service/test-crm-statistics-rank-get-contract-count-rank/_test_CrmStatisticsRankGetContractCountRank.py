import pytest
from config import ADMIN_URL


class TestCrmStatisticsRankGetContractCountRank:
    """获得签约合同数量排行榜"""

    @pytest.mark.smoke
    def test_CrmStatisticsRankGetContractCountRank(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-rank/get-contract-count-rank"
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
