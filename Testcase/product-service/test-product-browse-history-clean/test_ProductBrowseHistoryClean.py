import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductBrowseHistoryClean:
    """清空商品浏览记录"""

    @pytest.mark.smoke
    def test_ProductBrowseHistoryClean(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/browse-history/clean"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.delete(url, params=params, headers=headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
