import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductCategoryListByIds:
    """获得商品分类列表，指定编号"""

    @pytest.mark.smoke
    def test_ProductCategoryListByIds(self, api_session, login_tool):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/category/list-by-ids"
        params = {"ids": [48]}
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
