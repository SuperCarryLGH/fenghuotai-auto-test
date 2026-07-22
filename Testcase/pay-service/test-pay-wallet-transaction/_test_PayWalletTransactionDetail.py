import pytest
from config import ADMIN_URL


class TestPayWalletTransactionDetail:
    """获得钱包流水详情"""

    @pytest.mark.smoke
    def test_PayWalletTransactionDetail(self, api_session, station_token):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/detail"
        params = {"id": 15617637160, "walletType": 40}
        resp = api_session.get(url, params=params, headers={"Authorization": f"Bearer {station_token}"})
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
