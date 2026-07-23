import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductFavoriteExits:
    """检查是否收藏过商品"""

    @pytest.mark.smoke
    def test_ProductFavoriteExits(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/favorite/exits"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=headers))
