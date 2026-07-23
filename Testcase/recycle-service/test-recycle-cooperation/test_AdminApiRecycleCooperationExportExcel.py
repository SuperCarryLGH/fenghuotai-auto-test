import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_cooperation

common = load_common()
module_data = load_recycle_cooperation()


class Test_AdminApiRecycleCooperationExportExcel:
    """admin导出回收合作方Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleCooperationExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/cooperation/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)

        assert resp.status_code == 200

        assert len(resp.content) > 0
