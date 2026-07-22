import pytest
from config import APP_URL


class TestCartDelete:
    """删除购物车商品"""

    @pytest.mark.smoke
    def test_CartDelete(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/cart/delete"
        params = {"id": 1}  # TODO: 替换为实际要删除的 ID
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
