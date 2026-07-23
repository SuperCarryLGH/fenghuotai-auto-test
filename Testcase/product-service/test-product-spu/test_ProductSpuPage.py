import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductSpuPage:
    """获得商品 SPU 分页"""

    @pytest.mark.smoke
    def test_ProductSpuPage(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/spu/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=headers))
