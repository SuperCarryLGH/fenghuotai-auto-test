
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_sign,load_users

common = load_common()
module_data = load_recycle_station_sign()
users = load_users()


class Test_AdminApiRecycleActivityGroupDeleteList:
    """批量删除活动组"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityGroupDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-group/delete-list"
        body = {
            "ids": 9999,
        }
        resp = api_session.delete(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
