import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemPermissionAssignRoleMenu:
    """赋予角色菜单"""

    @pytest.mark.smoke
    def test_AdminApiSystemPermissionAssignRoleMenu(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/permission/assign-role-menu"
        body = {"roleId": 1, "menuIds": [1, 2, 3]}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
