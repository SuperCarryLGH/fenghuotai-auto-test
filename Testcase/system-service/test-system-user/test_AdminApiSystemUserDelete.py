import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemUserDelete:
    """删除用户"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/delete"
        resp = api_session.delete(url, params={"id": 2147483647}, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        print(r)
