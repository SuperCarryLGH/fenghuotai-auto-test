import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleStationClueExportExcel:
    """admin导出网点线索Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueExportExcel(self, api_session, station_user_ctx):
        b_headers, _, _ = station_user_ctx
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=b_headers)

        assert resp.status_code == 200
        assert len(resp.content) > 0
