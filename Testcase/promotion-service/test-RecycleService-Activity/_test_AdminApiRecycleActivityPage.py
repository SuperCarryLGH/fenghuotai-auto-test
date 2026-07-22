import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
module_data = load_recycle_activity()


class Test_AdminApiRecycleActivityPage:
    """admin回收活动分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
