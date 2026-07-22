import pytest
from config import APP_URL


class TestBrokerageUserGetRankByPrice:
    """获得分销用户排行（基于佣金）"""

    @pytest.mark.smoke
    def test_BrokerageUserGetRankByPrice(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-user/get-rank-by-price"
        params = {"id": "trade_app_brokerage_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
