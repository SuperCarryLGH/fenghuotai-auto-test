import pytest
from config import ADMIN_URL


class TestSystemMailTemplateDelete:
    """删除邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateDelete(self, api_session, auth_headers, autotest_mail_template_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/delete"
        params = {"id": autotest_mail_template_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
