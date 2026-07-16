import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiPayWalletRechargeCreate:
    """创建钱包充值记录（发起充值）"""

    @pytest.mark.smoke
    def test_AdminApiPayWalletRechargeCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge/create"
        params = {
            "payPrice": 10,
        }
        resp = api_session.post(url, json=params, headers=auth_headers)
        assert resp.status_code == 200
