import pytest
import time
from Common.login import Login
from config import APP_URL


class TestMemberSocialUserGet:
    """获得社交用户"""

    @pytest.mark.smoke
    def test_MemberSocialUserGet(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/member/social-user/get"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
