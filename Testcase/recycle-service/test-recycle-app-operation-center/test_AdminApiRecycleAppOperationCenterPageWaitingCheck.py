import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterPageWaitingCheck:
    """admin待验货分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterPageWaitingCheck(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/page-waiting-check"
        params = {"pageNo": common['common']['page']['pageNo'], "pageSize": common['common']['page']['pageSize']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
