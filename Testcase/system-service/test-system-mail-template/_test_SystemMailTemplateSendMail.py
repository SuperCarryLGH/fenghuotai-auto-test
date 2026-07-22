import pytest
from config import ADMIN_URL


class TestSystemMailTemplateSendMail:
    """发送短信"""

    @pytest.mark.smoke
    def test_SystemMailTemplateSendMail(self, api_session, auth_headers, autotest_mail_template_id):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/send-mail"
        body = {"toMails": ["autotest@test.com"], "ccMails": [], "bccMails": [], "templateCode": "AUTOTEST_MAIL"}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
