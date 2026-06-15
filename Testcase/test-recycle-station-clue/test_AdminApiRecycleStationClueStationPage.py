import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueStationPage:
    """admin站点分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueStationPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/station-page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
