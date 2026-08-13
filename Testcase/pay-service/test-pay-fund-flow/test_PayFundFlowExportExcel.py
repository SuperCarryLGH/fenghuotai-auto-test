import pytest
from config import ADMIN_URL


class TestPayFundFlowExportExcel:
    """导出资金流水 Excel"""

    @pytest.mark.smoke
    def test_PayFundFlowExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
