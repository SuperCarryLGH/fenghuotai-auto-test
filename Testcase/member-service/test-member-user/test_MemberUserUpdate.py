import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserUpdate:
    """更新会员用户"""

    @pytest.mark.smoke
    def test_MemberUserUpdate(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/update"
        body = {"id": 2074701659722608641, "nickname": f"更新用户_194200", "status": 0}
        ok(api_session.put(url, json=body, headers=headers))
