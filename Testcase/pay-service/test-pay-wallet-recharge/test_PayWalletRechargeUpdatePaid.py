import pytest
from config import ADMIN_URL


class TestPayWalletRechargeUpdatePaid:
    """更新钱包充值为已充值"""

    @pytest.mark.smoke
    def test_PayWalletRechargeUpdatePaid(self, api_session, station_token):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge/update-paid"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": "pay_wallet_recharge_id"}  # 来自 conftest fixture
        # resp = api_session.post(url, json=body, headers={"Authorization": f"Bearer {station_token}"})
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
