import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemUserUpdateStatus:
    """修改用户状态"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/update-status"
        body = {"id": common['common']['id']['valid'], "status": common['common']['status']['enabled']}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
