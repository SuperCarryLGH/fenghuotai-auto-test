import pytest
from config import ADMIN_URL


class TestSystemRoleGet:
    """获得角色信息"""

    @pytest.mark.smoke
    def test_SystemRoleGet(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/get"
        r = ok(api_session.get(url, params={"id": autotest_role_id}, headers=auth_headers))
        print(r)
