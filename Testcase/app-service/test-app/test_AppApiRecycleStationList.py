import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_station, load_page, load_common
station = load_station()
page = load_page()
common = load_common()

class TestAppApiRecycleStationList:
    """用户 APP - 根据类型查询站点列表（分页精简）"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationList(self, api_session, login_tool, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/station/list"
        params = {
            "type": station["station"]["type"],
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            }

        ok(api_session.get(url, headers=headers,params=params))