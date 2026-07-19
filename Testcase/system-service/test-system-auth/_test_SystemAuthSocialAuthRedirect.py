import pytest
from config import ADMIN_URL


class TestSystemAuthSocialAuthRedirect:
    """社交授权的跳转"""

    @pytest.mark.smoke
    def test_SystemAuthSocialAuthRedirect(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/social-auth-redirect"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
