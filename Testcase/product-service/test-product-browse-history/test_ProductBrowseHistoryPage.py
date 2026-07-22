import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductBrowseHistoryPage:
    """获得商品浏览记录分页"""

    @pytest.mark.smoke
    def test_ProductBrowseHistoryPage(self, api_session, login_tool):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/browse-history/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
