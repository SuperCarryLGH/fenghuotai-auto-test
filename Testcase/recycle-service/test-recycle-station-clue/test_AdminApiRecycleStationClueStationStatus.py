import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueStationStatus:
    """admin站点状态"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueStationStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/station-status"
        body = {"id": common['common']['id']['valid'], "status": common['common']['status']['enabled']}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
