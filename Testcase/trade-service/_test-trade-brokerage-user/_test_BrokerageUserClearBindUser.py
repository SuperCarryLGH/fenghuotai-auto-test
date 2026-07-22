import pytest
from config import ADMIN_URL


class TestBrokerageUserClearBindUser:
    """清除推广员"""

    @pytest.mark.smoke
    def test_BrokerageUserClearBindUser(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/brokerage-user/clear-bind-user"
        body = {"id": "trade_brokerage_user_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
