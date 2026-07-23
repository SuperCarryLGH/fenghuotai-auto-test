import pytest
from config import ADMIN_URL


class TestPayWalletGetRechargeDetail:
    """获得充值结果详情"""

    @pytest.mark.smoke
    def test_PayWalletGetRechargeDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/get-recharge-detail"
        params = {"rechargeId": 2079806408323100674}
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
