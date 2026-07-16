import pytest
from config import APP_URL


class TestBrokerageUserBind:
    """绑定推广员"""

    @pytest.mark.smoke
    def test_BrokerageUserBind(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-user/bind"
        body = {"id": "trade_app_brokerage_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
