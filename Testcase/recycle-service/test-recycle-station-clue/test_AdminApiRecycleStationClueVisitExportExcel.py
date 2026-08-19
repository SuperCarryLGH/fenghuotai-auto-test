import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleStationClueVisitExportExcel:
    """admin导出网点线索拜访记录Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueVisitExportExcel(self, api_session, station_user_ctx):
        b_headers, _, _ = station_user_ctx
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=b_headers)

        assert resp.status_code == 200
        assert len(resp.content) > 0
