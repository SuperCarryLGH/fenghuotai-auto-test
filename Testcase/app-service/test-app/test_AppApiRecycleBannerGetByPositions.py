import time
import pytest
from config import APP_URL
from Common.loader import load_station, load_common
from Common.login import Login
station = load_station()
common = load_common()

class TestAppApiRecycleBannerGetByPositions:
    """用户 APP - 根据位置获取banner"""

    def test_AppApiRecycleBannerGetByPositions(self, api_session, login_tool, ok):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/banner/get-by-positions"
        params = {
                    "positions": 1,
            }

        ok(api_session.get(url, headers=headers, params=params))