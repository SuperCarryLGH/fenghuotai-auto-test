import pytest
import random
from config import ADMIN_URL
from datetime import datetime
from Common.loader import load_common, load_recycle_activity, load_users, save_yaml

common = load_common()
activity_msg = load_recycle_activity()
users = load_users()


class Test_AdminApiRecycleHelpRecordCreate:
    """创建活动助力明细"""

    @pytest.mark.smoke
    def test_AdminApiRecycleHelpRecordCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-help-record/create"
        record_id = random.randint(100, 1000)
        record_id2 = random.randint(100, 1000)
        record_id3 = random.randint(100, 1000)
        body = {
                  "id": record_id,
                  "activityId": activity_msg['report_msg']['activity_id'],
                  "activityRecordId": activity_msg['report_msg']['activity_id'],
                  "helperUserId": users['users']['normal_user']['id'],
                  "helpTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  "remark": ""
                }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        save_yaml("help_record.yaml", {"id": record_id,"id2": record_id2,"id3": record_id3})
        print(r)
