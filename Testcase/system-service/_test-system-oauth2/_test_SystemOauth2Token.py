import pytest
from config import ADMIN_URL


class TestSystemOauth2Token:
    """获得访问令牌"""

    @pytest.mark.smoke
    def test_SystemOauth2Token(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2/token"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
