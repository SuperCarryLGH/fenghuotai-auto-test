import pytest
from config import ADMIN_URL
import random


class Test_AdminApiRecycleActivityHelpRecordPage:
    """获得活动助力明细分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityHelpRecordPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-help-record/page"
        body = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
