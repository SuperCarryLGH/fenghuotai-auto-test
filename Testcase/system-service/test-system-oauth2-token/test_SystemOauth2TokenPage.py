import pytest
from config import ADMIN_URL


class TestSystemOauth2TokenPage:
    """获得访问令牌分页"""

    @pytest.mark.smoke
    def test_SystemOauth2TokenPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-token/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
