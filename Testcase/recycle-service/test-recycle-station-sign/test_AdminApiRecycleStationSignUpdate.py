import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_sign

common = load_common()
module_data = load_recycle_station_sign()


class Test_AdminApiRecycleStationSignUpdate:
    """admin更新回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationSignUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/update"
        suffix = str(int(time.time()))
        body = {"id": module_data['station_sign']['id'], "name": f"{module_data['station_sign']['update_name']}_{suffix}", "status": common['common']['status']['enabled']}
        ok(api_session.put(url, json=body, headers=auth_headers))
