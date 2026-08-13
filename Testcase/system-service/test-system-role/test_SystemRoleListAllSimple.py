import pytest
from config import ADMIN_URL


class TestSystemRoleListAllSimple:
    """获取角色精简信息列表"""

    @pytest.mark.smoke
    def test_SystemRoleListAllSimple(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/list-all-simple"
        r = ok(api_session.get(url, headers=auth_headers))
        print(r)
