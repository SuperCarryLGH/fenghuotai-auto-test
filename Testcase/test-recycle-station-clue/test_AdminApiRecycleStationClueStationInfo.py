import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueStationInfo:
    """admin站点信息"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueStationInfo(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/station-info"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
