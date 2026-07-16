import pytest
from config import ADMIN_URL


class TestSystemOauth2ClientUpdate:
    """更新 OAuth2 客户端"""

    @pytest.mark.smoke
    def test_SystemOauth2ClientUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-client/update"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
