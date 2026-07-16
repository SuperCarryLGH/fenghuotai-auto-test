import pytest
from config import ADMIN_URL


class TestSystemUserDelete:
    """删除用户"""

    @pytest.mark.smoke
    def test_SystemUserDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
