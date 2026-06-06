import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiPayWalletRechargeCreate:
    """admin获取角色信息"""

    @pytest.mark.smoke
    def test_AdminApiPayWalletRechargeCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge/create"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
#test_AdminApiPayWalletRechargeCreate.py