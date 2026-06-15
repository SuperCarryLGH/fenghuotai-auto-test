import pytest
import random
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
report_msg = load_recycle_activity


class Test_AdminApiRecycleActivityReportCreate:
    """创建活动报告"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityReportCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-report/create"
        body = {
                  "id": 2000,#自增的ID 必填
                  "activityGroupId": report_msg['report_msg']['activity'],#	活动组ID,示例值(1)
                  "activityId": report_msg['report_msg']['activityId'],#	活动ID,示例值(1)
                  "userId": report_msg['report_msg']['userId'],#	报告创建人,示例值(10001)
                  "title": report_msg['report_msg']['title'],#报告标题
                  "coverImage": report_msg['report_msg']['coverImage'],
                  "content": report_msg['report_msg']['content'],
                  "status": report_msg['report_msg']['status'],
                  "remark": ""
                }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
