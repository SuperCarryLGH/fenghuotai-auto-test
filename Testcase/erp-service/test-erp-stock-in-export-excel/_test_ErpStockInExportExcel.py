import pytest
from config import ADMIN_URL


class TestErpStockInExportExcel:
    """导出其它入库单 Excel"""

    @pytest.mark.smoke
    def test_ErpStockInExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/stock-in/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
