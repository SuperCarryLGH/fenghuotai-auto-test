import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_users, load_common
users = load_users()
common = load_common()

class TestAppApiRecycleActivityDetail:
    """用户 APP - 发送手机验证码 Request VO"""

    @pytest.mark.smoke
    def test_AppApiRecycleActivityDetail(self, api_session, login_tool, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/activity/detail"
        params = {
                    "id": common['common']['id']['valid']
            }

        ok(api_session.get(url, headers=headers,params=params))