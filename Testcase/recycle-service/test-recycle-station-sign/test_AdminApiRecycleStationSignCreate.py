import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_sign

common = load_common()
module_data = load_recycle_station_sign()


class Test_AdminApiRecycleStationSignCreate:
    """admin创建回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationSignCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/create"
        suffix = str(int(time.time()))
        body = {"name": f"{module_data['station_sign']['name']}_{suffix}", "status": common['common']['status']['enabled']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
