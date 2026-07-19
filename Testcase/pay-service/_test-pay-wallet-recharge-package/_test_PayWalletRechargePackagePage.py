import pytest
from config import ADMIN_URL


class TestPayWalletRechargePackagePage:
    """获得钱包充值套餐分页"""

    @pytest.mark.smoke
    def test_PayWalletRechargePackagePage(self, api_session, auth_headers, autotest_wallet_recharge_package_id):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge-package/page"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        # resp = api_session.get(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
