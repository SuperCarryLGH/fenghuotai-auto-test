import pytest
from config import APP_URL


class TestMemberAuthSzdLogin:
    """苏周到授权登录"""

    @pytest.mark.smoke
    def test_MemberAuthSzdLogin(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/szd-login"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
