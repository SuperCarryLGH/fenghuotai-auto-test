import pytest
from config import ADMIN_URL


class TestSystemMailTemplateUpdate:
    """修改邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateUpdate(self, api_session, auth_headers, autotest_mail_template_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/update"
        import time
        body = {"id": autotest_mail_template_id, "name": f"mailtpl_{int(time.time())}", "code": f"CODE_{int(time.time())}", "accountId": 1, "title": "autotest_updated", "content": "autotest content", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
