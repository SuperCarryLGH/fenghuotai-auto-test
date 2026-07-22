import pytest
from config import APP_URL


class TestMemberAuthSocialAuthRedirect:
    """社交授权的跳转"""

    @pytest.mark.smoke
    def test_MemberAuthSocialAuthRedirect(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/social-auth-redirect"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
