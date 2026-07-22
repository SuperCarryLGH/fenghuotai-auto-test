import pytest
from config import ADMIN_URL


class TestPayFundUpdate:
    """更新支付资金"""

    @pytest.mark.smoke
    def test_PayFundUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund/update"
        body = {
            "id": 2068869977784700952,
            "fundType": 20,
            "orgId": 2074701657159761922,
            "totalFund": 10000,
            "wechatFund": 5000,
            "alipayFund": 5000,
            "allocableFund" : 0,
            "allocatedFund" : 0,
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
