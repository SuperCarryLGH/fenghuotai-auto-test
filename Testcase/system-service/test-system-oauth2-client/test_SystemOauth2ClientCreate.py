import pytest
from config import ADMIN_URL


class TestSystemOauth2ClientCreate:
    """创建 OAuth2 客户端"""

    @pytest.mark.smoke
    def test_SystemOauth2ClientCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-client/create"
        body = {"clientId": f"client_194199", "name": f"客户端_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
