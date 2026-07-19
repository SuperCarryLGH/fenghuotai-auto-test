import pytest
from config import ADMIN_URL


class TestPayWalletRechargePackageCreate:
    """创建钱包充值套餐"""

    @pytest.mark.smoke
    def test_PayWalletRechargePackageCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge-package/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"name": f"autotest_194200", "status": 0}
        # resp = api_session.post(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
