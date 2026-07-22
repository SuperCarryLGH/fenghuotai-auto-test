import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_activity

common = load_common()
module_data = load_recycle_activity()


class Test_AdminApiRecycleActivityGet:
    """admin获取回收活动详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleActivityGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/activity/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
