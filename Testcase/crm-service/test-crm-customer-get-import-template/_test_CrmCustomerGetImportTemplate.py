import pytest
from config import ADMIN_URL


class TestCrmCustomerGetImportTemplate:
    """获得导入客户模板"""

    @pytest.mark.smoke
    def test_CrmCustomerGetImportTemplate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/get-import-template"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
