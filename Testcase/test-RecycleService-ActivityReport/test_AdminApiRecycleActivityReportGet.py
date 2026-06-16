import pytest
import random
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
report_msg = load_recycle_activity


class Test_AdminApiRecycleActivityReportGet:
    """获取活动报告"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityReportGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-report/get"
        body = {
                  "id": random.randint(1, 3),
                }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
