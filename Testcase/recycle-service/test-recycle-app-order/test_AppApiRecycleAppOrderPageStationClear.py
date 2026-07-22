import pytest
import time
from config import APP_URL
from Common.loader import load_common
from Common.login import Login

common = load_common()


class Test_AppApiRecycleAppOrderPageStationClear:
    """APP站点清洁分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderPageStationClear(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/recycle/app/order/page-station-clear"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
