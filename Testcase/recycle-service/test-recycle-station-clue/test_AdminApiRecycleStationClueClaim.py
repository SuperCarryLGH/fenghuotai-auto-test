import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueClaim:
    """admin认领线索"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueClaim(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/claim"
        body = {"id": common['common']['id']['valid']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
