import pytest
from config import ADMIN_URL


class TestProductBrandUpdate:
    """更新品牌"""

    @pytest.mark.smoke
    def test_ProductBrandUpdate(self, api_session, auth_headers, autotest_brand_id, ok):
        url = f"{ADMIN_URL}/admin-api/product/brand/update"
        body = {"id": autotest_brand_id, "name": "autotest_brand_updated", "picUrl": "", "sort": 0, "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
