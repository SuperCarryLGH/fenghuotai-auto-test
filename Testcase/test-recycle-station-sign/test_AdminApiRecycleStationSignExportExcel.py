import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_sign

common = load_common()
module_data = load_recycle_station_sign()


class Test_AdminApiRecycleStationSignExportExcel:
    """admin导出回收站点签约Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationSignExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
