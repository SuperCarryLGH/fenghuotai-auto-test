import pytest
from config import ADMIN_URL


class TestSystemSmsLogGet:
    """获得短信日志"""

    @pytest.mark.smoke
    def test_SystemSmsLogGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/sms-log/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        ok(api_session.get(url, params=params, headers=auth_headers))
