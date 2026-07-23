import pytest
from config import ADMIN_URL


class TestPayWalletTransactionWallettranpage:
    """获得钱包流水分页-新"""

    @pytest.mark.smoke
    def test_PayWalletTransactionWallettranpage(self, api_session, station_token, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/walletTranPage"
        params = {"pageNo": 1, "pageSize": 10}
        resp = api_session.get(url, params=params, headers={"Authorization": f"Bearer {station_token}"})
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
