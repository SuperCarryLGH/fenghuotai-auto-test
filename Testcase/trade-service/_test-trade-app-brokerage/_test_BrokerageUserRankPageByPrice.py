import pytest
from config import APP_URL


class TestBrokerageUserRankPageByPrice:
    """获得分销用户排行分页（基于佣金）"""

    @pytest.mark.smoke
    def test_BrokerageUserRankPageByPrice(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-user/rank-page-by-price"
        params = {"pageNo": 1, "pageSize": 10}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
