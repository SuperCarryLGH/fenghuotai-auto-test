import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_express

common = load_common()
module_data = load_recycle_station_express()


class Test_AdminApiRecycleStationExpressUpdate:
    """admin更新回收站快递单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExpressUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/express/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"{module_data['station_express']['update_name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
