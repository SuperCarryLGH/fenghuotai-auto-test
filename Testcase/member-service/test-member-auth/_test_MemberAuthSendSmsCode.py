import time
import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAuthSendSmsCode:
    """发送手机验证码 — APP 端"""

    @pytest.mark.smoke
    def test_MemberAuthSendSmsCode(self, api_session):
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000))}
        url = f"{APP_URL}/app-api/member/auth/send-sms-code"
        body = {"mobile": "15617637160", "scene": 1}
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
