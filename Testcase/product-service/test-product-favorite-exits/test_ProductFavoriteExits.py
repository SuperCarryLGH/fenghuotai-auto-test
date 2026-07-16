import pytest
from config import APP_URL


class TestProductFavoriteExits:
    """检查是否收藏过商品"""

    @pytest.mark.smoke
    def test_ProductFavoriteExits(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/favorite/exits"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
