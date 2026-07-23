import pytest
from config import ADMIN_URL


class TestSystemMailAccountCreate:
    """创建邮箱账号"""

    @pytest.mark.smoke
    def test_SystemMailAccountCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/create"
        body = {"mail": f"test_194199@test.com", "username": f"test_194199", "password": "123456", "host": "smtp.test.com", "port": 465, "starttlsEnable": False, "sslEnable": False, "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
