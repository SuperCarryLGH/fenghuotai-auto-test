import pytest
from config import APP_URL


class TestProductCategoryListByIds:
    """获得商品分类列表，指定编号"""

    @pytest.mark.smoke
    def test_ProductCategoryListByIds(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/category/list-by-ids"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
