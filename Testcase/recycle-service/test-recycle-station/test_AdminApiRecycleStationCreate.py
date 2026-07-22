import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station

common = load_common()
module_data = load_recycle_station()


class Test_AdminApiRecycleStationCreate:
    """admin创建回收站点"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{module_data['station']['name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
