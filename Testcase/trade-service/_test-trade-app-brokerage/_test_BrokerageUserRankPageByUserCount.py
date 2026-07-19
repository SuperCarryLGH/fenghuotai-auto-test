import pytest
from config import APP_URL


class TestBrokerageUserRankPageByUserCount:
    """获得分销用户排行分页（基于用户量）"""

    @pytest.mark.smoke
    def test_BrokerageUserRankPageByUserCount(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-user/rank-page-by-user-count"
        params = {"pageNo": 1, "pageSize": 10}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
