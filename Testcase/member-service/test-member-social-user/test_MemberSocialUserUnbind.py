import pytest
from config import APP_URL


class TestMemberSocialUserUnbind:
    """取消社交绑定"""

    @pytest.mark.smoke
    def test_MemberSocialUserUnbind(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/social-user/unbind"
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
