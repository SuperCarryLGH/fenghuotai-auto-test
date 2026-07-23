import pytest
from config import ADMIN_URL


class TestSystemSmsLogPage:
    """获得短信日志分页"""

    @pytest.mark.smoke
    def test_SystemSmsLogPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/sms-log/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
