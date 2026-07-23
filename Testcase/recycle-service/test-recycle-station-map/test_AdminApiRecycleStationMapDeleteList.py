import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_map

common = load_common()
module_data = load_recycle_station_map()


class Test_AdminApiRecycleStationMapDeleteList:
    """admin批量删除回收站点地图"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationMapDeleteList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/map/delete-list"
        params = {"ids": common['common']['id']['invalid']}
        ok(api_session.delete(url, params=params, headers=auth_headers))
