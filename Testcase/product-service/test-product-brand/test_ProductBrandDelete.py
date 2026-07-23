import pytest
from config import ADMIN_URL


class TestProductBrandDelete:
    """删除品牌"""

    @pytest.mark.smoke
    def test_ProductBrandDelete(self, api_session, auth_headers, autotest_brand_id, ok):
        url = f"{ADMIN_URL}/admin-api/product/brand/delete"
        params = {"id": autotest_brand_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
