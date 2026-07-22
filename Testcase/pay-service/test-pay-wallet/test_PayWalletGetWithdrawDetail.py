import pytest
from config import ADMIN_URL


class TestPayWalletGetWithdrawDetail:
    """获得提现结果详情"""

    @pytest.mark.smoke
    def test_PayWalletGetWithdrawDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/get-withdraw-detail"
        params = {"withdrawId": 15617637160}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
