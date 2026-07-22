import pytest
from config import ADMIN_URL


class TestErpSaleOrderExportExcel:
    """导出销售订单 Excel"""

    @pytest.mark.smoke
    def test_ErpSaleOrderExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/sale-order/export-excel"
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
