import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_map

common = load_common()
module_data = load_recycle_station_map()


class Test_AdminApiRecycleStationMapExportExcel:
    """admin导出回收站点地图Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationMapExportExcel(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/map/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        ok(api_session.get(url, params=params, headers=auth_headers))
