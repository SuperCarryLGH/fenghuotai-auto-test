import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_map

common = load_common()
module_data = load_recycle_station_map()


class Test_AdminApiRecycleStationMapGet:
    """admin获取回收站点地图详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationMapGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/map/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
