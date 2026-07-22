import pytest
from config import APP_URL


class TestCartUpdateSelected:
    """更新购物车商品选中"""

    @pytest.mark.smoke
    def test_CartUpdateSelected(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/cart/update-selected"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
