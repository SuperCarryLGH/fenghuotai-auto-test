import pytest
from config import ADMIN_URL


class TestCrmStatisticsRankGetContactsCountRank:
    """获得新增联系人数排行榜"""

    @pytest.mark.smoke
    def test_CrmStatisticsRankGetContactsCountRank(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-rank/get-contacts-count-rank"
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
