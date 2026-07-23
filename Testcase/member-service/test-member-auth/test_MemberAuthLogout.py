import pytest
import time
from Common.login import Login
from config import APP_URL


class TestMemberAuthLogout:
    """登出系统"""

    @pytest.mark.smoke
    def test_MemberAuthLogout(self, api_session, login_tool, ok):
        url = f"{APP_URL}/app-api/member/auth/logout"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        body = {"id": 1}  # TODO: 补充参数
        ok(api_session.post(url, json=body, headers=headers))
