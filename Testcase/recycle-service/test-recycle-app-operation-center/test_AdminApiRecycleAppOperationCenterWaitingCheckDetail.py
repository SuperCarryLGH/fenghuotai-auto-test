import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterWaitingCheckDetail:
    """admin待验货详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterWaitingCheckDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/waiting-check-detail"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
