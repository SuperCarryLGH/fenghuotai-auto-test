import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductCategoryList:
    """获得商品分类列表"""

    @pytest.mark.smoke
    def test_ProductCategoryList(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/category/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=headers))
