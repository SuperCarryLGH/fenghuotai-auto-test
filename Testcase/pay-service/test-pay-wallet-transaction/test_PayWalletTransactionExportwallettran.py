import pytest
from config import ADMIN_URL


class TestPayWalletTransactionExportwallettran:
    """获得钱包流水导出"""

    @pytest.mark.smoke
    def test_PayWalletTransactionExportwallettran(self, api_session, station_token):
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/exportWalletTran"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers={"Authorization": f"Bearer {station_token}"})
        assert resp.status_code == 200 and len(resp.content) > 0
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
