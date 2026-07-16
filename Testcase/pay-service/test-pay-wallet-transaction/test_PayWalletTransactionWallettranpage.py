import pytest
from config import ADMIN_URL


class TestPayWalletTransactionWallettranpage:
    """获得钱包流水分页-新"""

    @pytest.mark.smoke
    def test_PayWalletTransactionWallettranpage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/walletTranPage"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
