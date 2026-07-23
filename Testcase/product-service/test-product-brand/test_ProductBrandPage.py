import pytest
from config import ADMIN_URL


class TestProductBrandPage:
    """获得品牌分页"""

    @pytest.mark.smoke
    def test_ProductBrandPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/product/brand/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
