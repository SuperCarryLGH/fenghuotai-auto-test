import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductBrowseHistoryDelete:
    """删除商品浏览记录"""

    @pytest.mark.smoke
    def test_ProductBrowseHistoryDelete(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/browse-history/delete"
        body = {"spuIds": [1]}
        ok(api_session.delete(url, json=body, headers=headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
