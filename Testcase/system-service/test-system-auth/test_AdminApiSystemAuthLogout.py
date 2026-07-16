import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemAuthLogout:
    """登出系统"""

    @pytest.mark.smoke
    def test_AdminApiSystemAuthLogout(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/logout"
        resp = api_session.post(url, headers=auth_headers)
        assert resp.status_code == 200
