import pytest
from config import ADMIN_URL
import random


class Test_AdminApiRecycleActivityHelpRecordGet:
    """获得活动助力明细"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityHelpRecordGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-help-record/get"
        body = {
            "id": random.randint(1, 10),
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
