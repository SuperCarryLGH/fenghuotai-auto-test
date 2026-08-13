import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiSystemRoleUpdate:
    """修改角色"""

    @pytest.mark.smoke
    def test_AdminApiSystemRoleUpdate(self, api_session, auth_headers, autotest_role_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/update"
        suffix = str(int(time.time()))
        body = {
            "id": autotest_role_id,
            "name": f"更新角色_{suffix}",
            "code": f"UPDATE_ROLE_{suffix}",
            "sort": 2,
            "status": 0,
        }
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
