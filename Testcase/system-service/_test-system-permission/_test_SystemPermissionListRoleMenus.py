import pytest
from config import ADMIN_URL


class TestSystemPermissionListRoleMenus:
    """获得角色拥有的菜单编号"""

    @pytest.mark.smoke
    def test_SystemPermissionListRoleMenus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/permission/list-role-menus"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
