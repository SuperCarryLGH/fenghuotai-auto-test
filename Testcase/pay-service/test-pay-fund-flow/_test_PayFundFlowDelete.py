import pytest
from config import ADMIN_URL


class TestPayFundFlowDelete:
    """删除资金流水"""

    @pytest.mark.smoke
    def test_PayFundFlowDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/delete"
        params = {}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
