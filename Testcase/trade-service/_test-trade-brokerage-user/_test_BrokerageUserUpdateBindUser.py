import pytest
from config import ADMIN_URL


class TestBrokerageUserUpdateBindUser:
    """修改推广员"""

    @pytest.mark.smoke
    def test_BrokerageUserUpdateBindUser(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/brokerage-user/update-bind-user"
        body = {"id": "trade_brokerage_user_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
