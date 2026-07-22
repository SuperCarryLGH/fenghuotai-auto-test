import pytest
import time
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue
from Common.login import Login

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AppApiRecycleStationCluePoolPage:
    """APP线索池分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationCluePoolPage(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/recycle/clue/pool-page"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
