import pytest
from config import ADMIN_URL


class TestSystemSocialClientDeleteList:
    """批量删除社交客户端"""

    @pytest.mark.smoke
    def test_SystemSocialClientDeleteList(self, api_session, auth_headers, system_social_client_id):
        url = f"{ADMIN_URL}/admin-api/system/social-client/delete-list"
        params = {"ids": str(autotest_social_client_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
