import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductFavoriteDelete:
    """取消单个商品收藏"""

    @pytest.mark.smoke
    def test_ProductFavoriteDelete(self, api_session, login_tool, autotest_favorite_id):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/favorite/delete"
        body = {"spuId": 633}
        resp = api_session.delete(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
