import pytest
from config import ADMIN_URL


class TestErpProductSimpleList:
    """获得产品精简列表"""

    @pytest.mark.smoke
    def test_ErpProductSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/product/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
