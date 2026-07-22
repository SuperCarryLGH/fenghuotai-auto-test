import pytest
from config import ADMIN_URL


class TestErpStockRecordExportExcel:
    """导出产品库存明细 Excel"""

    @pytest.mark.smoke
    def test_ErpStockRecordExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/stock-record/export-excel"
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
