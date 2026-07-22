import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserUpdateMobileByWeixin:
    """---"""

    @pytest.mark.smoke
    def test_MemberUserUpdateMobileByWeixin(self, api_session, login_tool):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/update-mobile-by-weixin"
        body = {"code": "9999"}
        resp = api_session.put(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
