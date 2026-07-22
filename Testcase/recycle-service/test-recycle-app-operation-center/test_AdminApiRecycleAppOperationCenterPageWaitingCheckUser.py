import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterPageWaitingCheckUser:
    """admin待验货人员分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterPageWaitingCheckUser(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/page-waiting-check-user"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
