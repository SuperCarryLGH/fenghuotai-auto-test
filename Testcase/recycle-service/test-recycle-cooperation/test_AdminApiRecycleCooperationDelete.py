import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_cooperation

common = load_common()
module_data = load_recycle_cooperation()


class Test_AdminApiRecycleCooperationDelete:
    """admin删除回收合作方"""

    @pytest.mark.smoke
    def test_AdminApiRecycleCooperationDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/cooperation/delete"
        params = {"id": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
