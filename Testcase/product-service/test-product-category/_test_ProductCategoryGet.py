import pytest
from config import ADMIN_URL


class TestProductCategoryGet:
    """获得商品分类"""

    @pytest.mark.smoke
    def test_ProductCategoryGet(self, api_session, auth_headers, autotest_category_id):
        url = f"{ADMIN_URL}/admin-api/product/category/get"
        params = {"id": autotest_category_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
