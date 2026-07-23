import pytest
from config import ADMIN_URL


class TestSystemMailAccountDelete:
    """删除邮箱账号"""

    @pytest.mark.smoke
    def test_SystemMailAccountDelete(self, api_session, auth_headers, autotest_mail_account_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/delete"
        params = {"id": autotest_mail_account_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
