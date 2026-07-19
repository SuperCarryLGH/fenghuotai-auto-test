import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
module_data = load_recycle_activity()


class Test_AdminApiRecycleActivityExportExcel:
    """admin导出回收活动Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity/export-excel"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
