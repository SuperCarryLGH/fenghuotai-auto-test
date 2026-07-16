import pytest
from config import ADMIN_URL


class TestErpCustomerSimpleList:
    """获得客户精简列表"""

    @pytest.mark.smoke
    def test_ErpCustomerSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/customer/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
