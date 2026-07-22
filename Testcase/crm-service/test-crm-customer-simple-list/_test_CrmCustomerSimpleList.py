import pytest
from config import ADMIN_URL


class TestCrmCustomerSimpleList:
    """获取客户精简信息列表"""

    @pytest.mark.smoke
    def test_CrmCustomerSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
