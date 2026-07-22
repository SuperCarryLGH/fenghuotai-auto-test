import pytest
from config import ADMIN_URL


class TestSystemOauth2ClientDeleteList:
    """批量删除 OAuth2 客户端"""

    @pytest.mark.smoke
    def test_SystemOauth2ClientDeleteList(self, api_session, auth_headers, autotest_oauth2_client_id):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-client/delete-list"
        params = {"ids": str(autotest_oauth2_client_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
