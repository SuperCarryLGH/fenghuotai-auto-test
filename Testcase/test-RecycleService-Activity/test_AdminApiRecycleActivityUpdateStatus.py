import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
module_data = load_recycle_activity()


class Test_AdminApiRecycleActivityUpdateStatus:
    """admin更新回收活动状态"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity/update-status"
        body = {"id": common['common']['id']['valid'], "status": common['common']['status']['enabled']}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
