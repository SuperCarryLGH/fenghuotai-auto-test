import pytest
from config import APP_URL


class TestCartList:
    """查询用户的购物车列表"""

    @pytest.mark.smoke
    def test_CartList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/cart/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
