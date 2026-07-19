import pytest
from config import ADMIN_URL


class TestSystemOauth2TokenDelete:
    """删除访问令牌"""

    @pytest.mark.smoke
    def test_SystemOauth2TokenDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-token/delete"
        params = {"id": 1}  # TODO: 替换为实际要删除的 ID
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
