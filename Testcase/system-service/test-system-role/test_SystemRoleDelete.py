import pytest
from config import ADMIN_URL


class TestSystemRoleDelete:
    """删除角色"""

    @pytest.mark.smoke
    def test_SystemRoleDelete(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/delete"
        r = ok(api_session.delete(url, params={"id": autotest_role_id}, headers=auth_headers))
        print(r)
