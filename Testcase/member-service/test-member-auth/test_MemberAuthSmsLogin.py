import pytest
import time
from Common.login import Login
from config import APP_URL


class TestMemberAuthSmsLogin:
    """使用手机 + 验证码登录"""

    @pytest.mark.smoke
    def test_MemberAuthSmsLogin(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/member/auth/sms-login"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
