import pytest
from config import ADMIN_URL


class TestPayWalletGetWithdrawDetail:
    """获得提现结果详情"""

    @pytest.mark.smoke
    def test_PayWalletGetWithdrawDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/get-withdraw-detail"
        params = {"withdrawId": 2076606633096376322}
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
