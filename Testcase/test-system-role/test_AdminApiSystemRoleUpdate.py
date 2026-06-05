import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiSystemRoleUpdate:
    """admin修改角色"""

    @pytest.mark.smoke
    def test_AdminApiSystemRoleUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/role/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"更新角色_{suffix}",
            "code": f"UPDATE_ROLE_{suffix}",
            "sort": 2,
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
