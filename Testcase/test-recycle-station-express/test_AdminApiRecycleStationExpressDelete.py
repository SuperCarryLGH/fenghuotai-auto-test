import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_express

common = load_common()
module_data = load_recycle_station_express()


class Test_AdminApiRecycleStationExpressDelete:
    """admin删除回收站快递单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExpressDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/express/delete"
        params = {"id": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
