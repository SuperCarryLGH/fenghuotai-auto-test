import pytest
from config import APP_URL


class TestBrokerageWithdrawCreate:
    """创建分销提现"""

    @pytest.mark.smoke
    def test_BrokerageWithdrawCreate(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-withdraw/create"
        body = {"name": f"autotest_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
