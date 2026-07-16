import pytest
from config import ADMIN_URL


class TestSystemSocialClientGet:
    """获得社交客户端"""

    @pytest.mark.smoke
    def test_SystemSocialClientGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/social-client/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
