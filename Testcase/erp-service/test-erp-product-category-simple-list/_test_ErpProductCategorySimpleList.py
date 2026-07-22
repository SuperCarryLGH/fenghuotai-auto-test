import pytest
from config import ADMIN_URL


class TestErpProductCategorySimpleList:
    """获得产品分类精简列表"""

    @pytest.mark.smoke
    def test_ErpProductCategorySimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/product-category/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
