import pytest
from config import ADMIN_URL
import random
import datetime
from Common.loader import load_recycle_activity,load_users
report_msg = load_recycle_activity()
user = load_users()

class Test_AdminApiRecycleActivityHelpRecordUpdate:
    """更新活动助力明细"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityHelpRecordUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-help-record/update"
        body = {
                  "id": random.randint(100, 1000),
                  "activityId": report_msg['report_msg']['activityId'],
                  "activityRecordId": report_msg['report_msg']['activityRecordId'],
                  "helperUserId": user['users']['normal_user']['id'],
                  "helpTime": datetime.datetime.now(),
                  "remark": "",
                }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
