import random
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_page,load_recycle_activity

common = load_common()
page = load_page()
report_msg = load_recycle_activity()


class Test_AdminApiRecycleActivityRecordGet:
    """获得活动参与记录"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityRecordGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-record/get"
        body ={
            "id": random.randint(1, 100),
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
