import pytest
from datetime import datetime
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity,load_page

common = load_common()
page = load_page()
report_msg = load_recycle_activity


class Test_AdminApiRecycleActivityReportPage:
    """获取活动报告"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityReportPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-report/page"
        body = {
            "pageNo": page['page']['pageNo'],
            "pageSize": page['page']['pageSize'],
            "activityGroupId": report_msg['report_msg']['activityGroupId'],
            "activityId": report_msg['report_msg']['activityId'],
            "userId": report_msg['report_msg']['userId'],
            "title": report_msg['report_msg']['title'],
            "status": report_msg['report_msg']['status'],
            "createTime": datetime.now()
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
