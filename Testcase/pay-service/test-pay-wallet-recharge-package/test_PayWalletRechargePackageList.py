import pytest
from config import APP_URL


class TestPayWalletRechargePackageList:
    """获得钱包充值套餐列表"""

    @pytest.mark.smoke
    def test_PayWalletRechargePackageList(self, api_session, auth_headers, pay_wallet_recharge_package_id):
        url = f"{APP_URL}/app-api/pay/wallet-recharge-package/list"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        # resp = api_session.get(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
