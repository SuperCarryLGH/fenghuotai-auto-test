import pytest
from config import ADMIN_URL


class TestSystemOauth2TokenDeleteList:
    """批量删除访问令牌"""

    @pytest.mark.smoke
    def test_SystemOauth2TokenDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-token/delete-list"
        params = {"ids": "1,2,3"}  # TODO: 替换为实际 ID 列表
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
