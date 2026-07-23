import pytest
from config import ADMIN_URL


class TestPayFundFlowGet:
    """获得资金流水"""

    @pytest.mark.smoke
    def test_PayFundFlowGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/get"
        params = {
            "id":2077206234371321858,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
