import pytest
import random
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
report_msg = load_recycle_activity


class Test_AdminApiRecycleActivityReportDeleteList:
    """创建活动报告"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityReportDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-report/delete-list"
        body = {
                  "ids": 2000,
                }
        resp = api_session.delete(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
