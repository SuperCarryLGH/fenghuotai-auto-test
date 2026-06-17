import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiPayWalletRechargeRefund:
    """发起钱包充值退款"""

    @pytest.mark.smoke
    def test_AdminApiPayWalletRechargeRefund(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge/refund"
        params = {
            "id": 10, #钱包充值编号
        }
        resp = api_session.post(url, json=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
