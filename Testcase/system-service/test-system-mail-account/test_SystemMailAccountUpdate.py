import pytest
from config import ADMIN_URL


class TestSystemMailAccountUpdate:
    """修改邮箱账号"""

    @pytest.mark.smoke
    def test_SystemMailAccountUpdate(self, api_session, auth_headers, autotest_mail_account_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/update"
        body = {"id": autotest_mail_account_id, "mail": "autotest@autotest.com", "username": "autotest_updated", "password": "autotest123", "host": "smtp.autotest.com", "port": 465, "sslEnable": False, "starttlsEnable": False}
        ok(api_session.put(url, json=body, headers=auth_headers))
