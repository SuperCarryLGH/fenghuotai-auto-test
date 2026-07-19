import pytest
from config import APP_URL


class TestCartReset:
    """重置购物车商品"""

    @pytest.mark.smoke
    def test_CartReset(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/cart/reset"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
