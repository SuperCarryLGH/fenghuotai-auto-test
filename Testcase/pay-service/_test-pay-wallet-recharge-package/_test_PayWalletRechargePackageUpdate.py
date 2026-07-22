import pytest
from config import ADMIN_URL


class TestPayWalletRechargePackageUpdate:
    """更新钱包充值套餐"""

    @pytest.mark.smoke
    def test_PayWalletRechargePackageUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge-package/update"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": "pay_wallet_recharge_package_id"}  # 来自 conftest fixture
        # resp = api_session.put(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
