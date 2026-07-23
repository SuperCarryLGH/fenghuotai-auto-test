import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemUserDelete:
    """删除用户"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserDelete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/delete"
        params = {"id": common['common']['id']['invalid']}
        ok(api_session.delete(url, params=params, headers=auth_headers))
