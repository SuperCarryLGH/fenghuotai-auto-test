import pytest
from config import ADMIN_URL


class TestBrokerageUserGet:
    """获得分销用户"""

    @pytest.mark.smoke
    def test_BrokerageUserGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/brokerage-user/get"
        params = {"id": "trade_brokerage_user_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
