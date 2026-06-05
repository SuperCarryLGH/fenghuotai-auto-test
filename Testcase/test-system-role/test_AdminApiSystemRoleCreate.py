import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_role

common = load_common()
role_data = load_system_role()


class Test_AdminApiSystemRoleCreate:
    """admin创建角色"""

    @pytest.mark.smoke
    def test_AdminApiSystemRoleCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/role/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"测试角色_{suffix}",
            "code": f"{role_data['role']['create']['code']}_{suffix}",
            "sort": role_data['role']['create']['sort'],
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
