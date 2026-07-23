import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_cooperation

common = load_common()
module_data = load_recycle_cooperation()


class Test_AdminApiRecycleCooperationPage:
    """admin回收合作方分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleCooperationPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/cooperation/page"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
