import pytest
import time
from Common.login import Login
from config import APP_URL


class TestSignInRecordCreate:
    """签到"""

    @pytest.mark.smoke
    def test_SignInRecordCreate(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/member/sign-in/record/create"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        body = {"name": f"签到_194200", "point": 10, "status": 0}
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
