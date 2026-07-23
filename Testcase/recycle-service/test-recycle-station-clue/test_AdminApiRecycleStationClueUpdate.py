import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_station_clue

common = load_common()
clue_data = load_recycle_station_clue()


class Test_AdminApiRecycleStationClueUpdate:
    """admin更新回收站点线索"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/update"
        suffix = str(int(time.time()))
        body = {"id": clue_data['station_clue']['id'], "name": f"{clue_data['station_clue']['update_name']}_{suffix}", "status": common['common']['status']['enabled']}
        ok(api_session.put(url, json=body, headers=auth_headers))
