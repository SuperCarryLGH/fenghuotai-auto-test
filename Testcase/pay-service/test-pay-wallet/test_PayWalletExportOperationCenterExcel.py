import pytest
from config import ADMIN_URL


class TestPayWalletExportOperationCenterExcel:
    """导出分拣中心钱包 Excel"""

    @pytest.mark.smoke
    def test_PayWalletExportOperationCenterExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/export-operation-center-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
