import pytest
from config import ADMIN_URL


class TestPayWalletTransactionExportwallettran:
    """获得钱包流水导出"""

    @pytest.mark.smoke
    def test_PayWalletTransactionExportwallettran(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/exportWalletTran"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
