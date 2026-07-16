import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_express

common = load_common()
module_data = load_recycle_station_express()


class Test_AdminApiRecycleStationExpressCreate:
    """admin创建回收站快递单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExpressCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/express/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{module_data['station_express']['name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
