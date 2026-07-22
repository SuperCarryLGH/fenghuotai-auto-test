import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserUpdateMobile:
    """---"""

    @pytest.mark.smoke
    def test_MemberUserUpdateMobile(self, api_session, login_tool):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/update-mobile"
        body = {"mobile": "15611111111", "code": "9999"}
        resp = api_session.put(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
