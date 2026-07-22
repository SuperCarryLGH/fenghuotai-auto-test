import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductBrowseHistoryDelete:
    """删除商品浏览记录"""

    @pytest.mark.smoke
    def test_ProductBrowseHistoryDelete(self, api_session, login_tool):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/browse-history/delete"
        params = {"id": 1}  # TODO: 替换为实际要删除的 ID
        resp = api_session.delete(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
