import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
module_data = load_recycle_activity()


class Test_AdminApiRecycleActivityUpdate:
    """admin更新回收活动"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"{module_data['activity']['update_name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
