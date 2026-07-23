import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_map

common = load_common()
module_data = load_recycle_station_map()


class Test_AdminApiRecycleStationMapUpdate:
    """admin更新回收站点地图"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationMapUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/map/update"
        suffix = str(int(time.time()))
        body = {"id": common['common']['id']['valid'], "name": f"{module_data['station_map']['update_name']}_{suffix}", "status": common['common']['status']['enabled']}
        ok(api_session.put(url, json=body, headers=auth_headers))
