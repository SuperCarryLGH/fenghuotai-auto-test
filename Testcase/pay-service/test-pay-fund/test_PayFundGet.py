import pytest
from config import ADMIN_URL


class TestPayFundGet:
    """获得支付资金"""

    @pytest.mark.smoke
    def test_PayFundGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund/get"
        params = {
            "id" : 3
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
