import pytest
from config import ADMIN_URL


class TestSystemRoleUpdate:
    """修改角色"""

    @pytest.mark.smoke
    def test_SystemRoleUpdate(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/update"
        body = {"id": autotest_role_id, "name": "autotest_role_update", "code": "AUTOTEST_ROLE_UPDATE", "sort": 0, "status": 0}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
