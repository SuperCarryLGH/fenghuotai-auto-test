import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AppApiRecycleClueMyPage:
    """APP我的线索分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleClueMyPage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/clue/my-page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
