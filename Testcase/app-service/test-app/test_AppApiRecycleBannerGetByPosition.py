import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_station, load_common
station = load_station()
common = load_common()

class TestAppApiRecycleBannerGetByPosition:
    """用户 APP - 根据位置获取banner"""

    @pytest.mark.smoke
    def test_AppApiRecycleBannerGetByPosition(self, api_session, login_tool, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/banner/get-by-position"
        params = {
                    "position": 1,
            }

        ok(api_session.get(url, headers=headers,params=params))