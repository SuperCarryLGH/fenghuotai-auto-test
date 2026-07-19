
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_page,load_recycle_activity

common = load_common()
page = load_page()
report_msg = load_recycle_activity()


class Test_AdminApiRecycleActivityRecordPageActivityOrder:
    """活动参与订单分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityRecordPageActivityOrder(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity-record/pageActivityOrder"
        body ={
            "pageNo": page["page"]["pageNo"],
            "pageSize": page["page"]["pageSize"],
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
