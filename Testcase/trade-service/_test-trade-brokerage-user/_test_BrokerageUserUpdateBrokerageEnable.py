import pytest
from config import ADMIN_URL


class TestBrokerageUserUpdateBrokerageEnable:
    """修改推广资格"""

    @pytest.mark.smoke
    def test_BrokerageUserUpdateBrokerageEnable(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/brokerage-user/update-brokerage-enable"
        body = {"id": "trade_brokerage_user_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
