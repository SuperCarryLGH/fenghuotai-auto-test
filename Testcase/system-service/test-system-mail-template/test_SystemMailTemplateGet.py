import pytest
from config import ADMIN_URL


class TestSystemMailTemplateGet:
    """获得邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateGet(self, api_session, auth_headers, autotest_mail_template_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/get"
        params = {"id": autotest_mail_template_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
