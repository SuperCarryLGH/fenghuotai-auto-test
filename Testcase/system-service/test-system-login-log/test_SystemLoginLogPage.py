import pytest
from config import ADMIN_URL


class TestSystemLoginLogPage:
    """获得登录日志分页列表"""

    @pytest.mark.smoke
    def test_SystemLoginLogPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/login-log/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
