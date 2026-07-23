import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterWaitingCheckDetailUser:
    """admin待验货人员详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterWaitingCheckDetailUser(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/waiting-check-detail-user"
        params = {"id": common['common']['id']['valid']}
        ok(api_session.get(url, params=params, headers=auth_headers))
