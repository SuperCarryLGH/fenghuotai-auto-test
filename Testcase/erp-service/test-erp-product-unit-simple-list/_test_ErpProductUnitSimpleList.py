import pytest
from config import ADMIN_URL


class TestErpProductUnitSimpleList:
    """获得产品单位精简列表"""

    @pytest.mark.smoke
    def test_ErpProductUnitSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/product-unit/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
