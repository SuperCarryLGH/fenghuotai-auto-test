import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemRoleDelete:
    """删除角色"""

    @pytest.mark.smoke
    def test_AdminApiSystemRoleDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/role/delete"
        resp = api_session.delete(url, params={"id": 2147483647}, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        print(r)
