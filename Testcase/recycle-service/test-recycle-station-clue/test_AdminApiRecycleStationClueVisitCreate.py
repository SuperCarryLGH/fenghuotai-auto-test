import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueVisitCreate:
    """admin创建回访"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueVisitCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/visit-create"
        suffix = str(int(time.time()))
        body = {"name": f"{clue_data['station_clue']['visit']['name']}_{suffix}", "status": common['common']['status']['enabled']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
