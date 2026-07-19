import pytest
from config import ADMIN_URL


class TestBrokerageUserCreate:
    """创建分销用户"""

    @pytest.mark.smoke
    def test_BrokerageUserCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/brokerage-user/create"
        body = {"name": f"autotest_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
