import pytest
from config import ADMIN_URL


class TestErpSupplierExportExcel:
    """导出供应商 Excel"""

    @pytest.mark.smoke
    def test_ErpSupplierExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/supplier/export-excel"
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
