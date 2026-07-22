import pytest
from config import ADMIN_URL


class TestProductBrandListAllSimple:
    """获取品牌精简信息列表"""

    @pytest.mark.smoke
    def test_ProductBrandListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/brand/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
