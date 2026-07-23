import pytest
from config import ADMIN_URL


class TestPayWalletExportStationExcel:
    """导出网点钱包 Excel"""

    @pytest.mark.smoke
    def test_PayWalletExportStationExcel(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/export-station-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
