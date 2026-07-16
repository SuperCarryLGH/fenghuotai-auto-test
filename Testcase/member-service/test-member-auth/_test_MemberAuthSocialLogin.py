import pytest
from config import APP_URL


class TestMemberAuthSocialLogin:
    """社交快捷登录，使用 code 授权码"""

    @pytest.mark.smoke
    def test_MemberAuthSocialLogin(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/social-login"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
