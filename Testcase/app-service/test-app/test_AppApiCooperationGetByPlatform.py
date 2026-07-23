import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_users, load_common
users = load_users()
common = load_common()

@pytest.mark.skip(reason="接口 404，待确认路径")
class TestAppApiCooperationGetByPlatform:
    """用户 APP - 发送手机验证码 Request VO"""

    @pytest.mark.smoke
    def test_AppApiCooperationGetByPlatform(self, api_session, login_tool, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/cooperation/getByPlatform"
        params = {
            "platform": "1",
            "channel":" "
            }

        ok(api_session.get(url, headers=headers,params=params))








#test_AppApiCooperationGetByPlatform