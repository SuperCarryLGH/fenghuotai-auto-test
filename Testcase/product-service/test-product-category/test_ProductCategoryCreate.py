import pytest
from config import ADMIN_URL


class TestProductCategoryCreate:
    """创建商品分类"""

    @pytest.mark.smoke
    def test_ProductCategoryCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/category/create"
        body = {"name": f"类目_194199", "sort": 0, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
