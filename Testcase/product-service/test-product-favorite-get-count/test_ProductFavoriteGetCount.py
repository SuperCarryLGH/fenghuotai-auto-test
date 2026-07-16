import pytest
from config import APP_URL


class TestProductFavoriteGetCount:
    """获得商品收藏数量"""

    @pytest.mark.smoke
    def test_ProductFavoriteGetCount(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/favorite/get-count"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
