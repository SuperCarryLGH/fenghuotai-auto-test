import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_station, load_common
station = load_station()
common = load_common()

class TestAppApiRecycleStationDetail:
    """用户 APP - 站点全量详情（基础信息+签约配置完整数据）"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationDetail(self, api_session, login_tool):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/station/detail"
        params = {
                    "id": station["station"]["id"],
            }

        resp = api_session.get(url, headers=headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)