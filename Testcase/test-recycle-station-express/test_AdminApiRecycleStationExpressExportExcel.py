import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_express

common = load_common()
module_data = load_recycle_station_express()


class Test_AdminApiRecycleStationExpressExportExcel:
    """admin导出回收站快递单Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationExpressExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/express/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
