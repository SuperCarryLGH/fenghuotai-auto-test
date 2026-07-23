import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductFavoriteGetCount:
    """获得商品收藏数量"""

    @pytest.mark.smoke
    def test_ProductFavoriteGetCount(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/favorite/get-count"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=headers))
