import pytest
from config import ADMIN_URL


class TestPayFundFlowCreate:
    """创建资金流水"""

    @pytest.mark.smoke
    def test_PayFundFlowCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/create"
        body = {}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
