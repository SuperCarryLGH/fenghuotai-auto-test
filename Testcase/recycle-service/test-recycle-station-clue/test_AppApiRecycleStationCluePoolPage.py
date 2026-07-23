import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AppApiRecycleStationCluePoolPage:
    """APP线索池分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationCluePoolPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/pool-page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
