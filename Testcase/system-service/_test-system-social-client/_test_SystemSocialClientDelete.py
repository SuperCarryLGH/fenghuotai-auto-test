import pytest
from config import ADMIN_URL


class TestSystemSocialClientDelete:
    """删除社交客户端"""

    @pytest.mark.smoke
    def test_SystemSocialClientDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/social-client/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
