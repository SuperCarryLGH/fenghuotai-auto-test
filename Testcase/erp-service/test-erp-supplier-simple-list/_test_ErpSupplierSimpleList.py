import pytest
from config import ADMIN_URL


class TestErpSupplierSimpleList:
    """获得供应商精简列表"""

    @pytest.mark.smoke
    def test_ErpSupplierSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/supplier/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
