import pytest
from config import ADMIN_URL


class TestPayFundFlowDeleteList:
    """批量删除资金流水"""

    @pytest.mark.smoke
    def test_PayFundFlowDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/delete-list"
        params = {}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
