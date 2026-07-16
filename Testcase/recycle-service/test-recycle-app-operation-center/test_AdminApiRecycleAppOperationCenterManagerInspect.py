import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterManagerInspect:
    """admin管理员验货"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterManagerInspect(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/manager-inspect"
        body = {"id": common['common']['id']['valid']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
