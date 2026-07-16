import pytest
from config import ADMIN_URL


class TestPayFundExportExcel:
    """导出分拣中心资金 Excel"""

    @pytest.mark.smoke
    def test_PayFundExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        print(resp)
