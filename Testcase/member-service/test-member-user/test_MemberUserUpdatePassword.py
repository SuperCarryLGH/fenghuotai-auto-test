import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserUpdatePassword:
    """---"""

    @pytest.mark.smoke
    def test_MemberUserUpdatePassword(self, api_session, login_tool):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/update-password"
        body = {"password": "autotest123"}
        resp = api_session.put(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
