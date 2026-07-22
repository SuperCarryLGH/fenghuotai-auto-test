import pytest
from config import ADMIN_URL


class TestSystemMailAccountGet:
    """获得邮箱账号"""

    @pytest.mark.smoke
    def test_SystemMailAccountGet(self, api_session, auth_headers, autotest_mail_account_id):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/get"
        params = {"id": autotest_mail_account_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
