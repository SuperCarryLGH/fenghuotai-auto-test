import pytest
from config import ADMIN_URL


class TestSystemPermissionListUserRoles:
    """获得管理员拥有的角色编号列表"""

    @pytest.mark.smoke
    def test_SystemPermissionListUserRoles(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/permission/list-user-roles"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
