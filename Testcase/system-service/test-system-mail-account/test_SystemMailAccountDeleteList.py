import pytest
from config import ADMIN_URL


class TestSystemMailAccountDeleteList:
    """批量删除邮箱账号"""

    @pytest.mark.smoke
    def test_SystemMailAccountDeleteList(self, api_session, auth_headers, autotest_mail_account_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/delete-list"
        params = {"ids": str(autotest_mail_account_id)}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
