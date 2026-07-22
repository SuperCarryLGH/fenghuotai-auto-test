import pytest
import time
from Common.login import Login
from config import APP_URL


class TestSignInRecordGetSummary:
    """获得个人签到统计"""

    @pytest.mark.smoke
    def test_SignInRecordGetSummary(self, api_session, login_tool, autotest_record_id):
        url = f"{APP_URL}/app-api/member/sign-in/record/get-summary"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        params = {"id": autotest_record_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
