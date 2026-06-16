import pytest
from config import ADMIN_URL
from Common.loader import load_yaml,load_page
page = load_page()



class Test_AdminApiRecycleActivityHelpRecordExportExcel:
    """导出活动助力明细 Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityHelpRecordExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-help-record/export-excel"
        body = {
            "pageNo":page['page']['pageNo'],
            "pageSize":page['page']['pageSize'],
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
