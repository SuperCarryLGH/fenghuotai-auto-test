import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_cooperation

common = load_common()
module_data = load_recycle_cooperation()


class Test_AdminApiRecycleCooperationGet:
    """admin获取回收合作方详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleCooperationGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/station/cooperation/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
