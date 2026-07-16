import pytest
from config import APP_URL


class TestMemberSocialUserGet:
    """获得社交用户"""

    @pytest.mark.smoke
    def test_MemberSocialUserGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/social-user/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
