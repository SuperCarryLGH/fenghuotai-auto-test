import pytest
from config import APP_URL


class TestMemberSocialUserBind:
    """社交绑定，使用 code 授权码"""

    @pytest.mark.smoke
    def test_MemberSocialUserBind(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/social-user/bind"
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
