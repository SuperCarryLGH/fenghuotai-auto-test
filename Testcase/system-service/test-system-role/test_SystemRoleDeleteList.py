import pytest
from config import ADMIN_URL


class TestSystemRoleDeleteList:
    """批量删除角色"""

    @pytest.mark.smoke
    def test_SystemRoleDeleteList(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/delete-list"
        r = ok(api_session.delete(url, params={"ids": str(autotest_role_id)}, headers=auth_headers))
        print(r)
