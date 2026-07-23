import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station

common = load_common()
module_data = load_recycle_station()


class Test_AdminApiRecycleStationExportExcel:
    """admin导出回收站点Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExportExcel(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        ok(api_session.get(url, params=params, headers=auth_headers))
