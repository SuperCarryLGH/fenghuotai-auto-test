import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemRoleDelete:
    """删除角色"""

    @pytest.mark.smoke
    def test_AdminApiSystemRoleDelete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/role/delete"
        params = {"id": common['common']['id']['invalid']}
        ok(api_session.delete(url, params=params, headers=auth_headers))
