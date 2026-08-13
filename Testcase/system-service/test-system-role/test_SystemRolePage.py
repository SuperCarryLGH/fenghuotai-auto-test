import pytest
from config import ADMIN_URL


class TestSystemRolePage:
    """获得角色分页"""

    @pytest.mark.smoke
    def test_SystemRolePage(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/page"
        r = ok(api_session.get(url, params={"pageNo": 1, "pageSize": 10}, headers=auth_headers))
        print(r)
