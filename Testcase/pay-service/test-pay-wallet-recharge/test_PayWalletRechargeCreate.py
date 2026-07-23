import pytest
from config import ADMIN_URL


class TestPayWalletRechargeCreate:
    """创建钱包充值记录（发起充值）"""

    @pytest.mark.smoke
    def test_PayWalletRechargeCreate(self, api_session, station_token):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-recharge/create"
        body = {
              "payPrice": 50,
              #"packageId": 1024,
              "userType": 2,
              #"bizType": 0,
              #"validPayPriceAndPackageId": True
            }
        ok(api_session.post(url, json=body, headers={"Authorization": f"Bearer {station_token}"}))
        r = resp.json()
        print(r)
        assert r["code"] == 0

