import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemPermissionAssignUserRole:
    """赋予用户角色"""

    @pytest.mark.smoke
    def test_AdminApiSystemPermissionAssignUserRole(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/permission/assign-user-role"
        body = {"userId": 1, "roleIds": [1]}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
