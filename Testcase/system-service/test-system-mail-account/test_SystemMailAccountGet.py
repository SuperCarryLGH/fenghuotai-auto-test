import pytest
from config import ADMIN_URL


class TestSystemMailAccountGet:
    """获得邮箱账号"""

    @pytest.mark.smoke
    def test_SystemMailAccountGet(self, api_session, auth_headers, autotest_mail_account_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/get"
        params = {"id": autotest_mail_account_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
