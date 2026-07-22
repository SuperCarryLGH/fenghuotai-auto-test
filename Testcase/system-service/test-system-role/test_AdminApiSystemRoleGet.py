import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiSystemRoleGet:
    """获得角色信息"""

    @pytest.mark.smoke
    def test_AdminApiSystemRoleGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/role/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
