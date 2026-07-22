import pytest
from config import ADMIN_URL


class TestCrmCustomerExportExcel:
    """导出客户 Excel"""

    @pytest.mark.smoke
    def test_CrmCustomerExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/export-excel"
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
