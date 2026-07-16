import pytest
from config import APP_URL


class TestProductFavoriteDelete:
    """取消单个商品收藏"""

    @pytest.mark.smoke
    def test_ProductFavoriteDelete(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/favorite/delete"
        params = {"id": "product_favorite_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
