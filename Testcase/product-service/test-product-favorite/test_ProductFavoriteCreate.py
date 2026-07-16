import pytest
from config import APP_URL


class TestProductFavoriteCreate:
    """添加商品收藏"""

    @pytest.mark.smoke
    def test_ProductFavoriteCreate(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/favorite/create"
        body = {"name": f"商品_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
