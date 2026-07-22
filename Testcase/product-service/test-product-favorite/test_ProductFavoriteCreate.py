import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductFavoriteCreate:
    """添加商品收藏"""

    @pytest.mark.smoke
    def test_ProductFavoriteCreate(self, api_session, login_tool):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/favorite/create"
        body = {"name": f"商品_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
