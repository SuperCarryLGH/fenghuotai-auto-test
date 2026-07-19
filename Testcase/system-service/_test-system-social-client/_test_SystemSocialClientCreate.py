import pytest
from config import ADMIN_URL


class TestSystemSocialClientCreate:
    """创建社交客户端"""

    @pytest.mark.smoke
    def test_SystemSocialClientCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/social-client/create"
        body = {"name": f"autotest_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
