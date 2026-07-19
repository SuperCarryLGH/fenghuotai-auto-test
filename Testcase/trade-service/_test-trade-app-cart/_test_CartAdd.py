import pytest
from config import APP_URL


class TestCartAdd:
    """添加购物车商品"""

    @pytest.mark.smoke
    def test_CartAdd(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/cart/add"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
