import pytest
from config import ADMIN_URL


class TestSystemSmsTemplateSendSms:
    """发送短信"""

    @pytest.mark.smoke
    def test_SystemSmsTemplateSendSms(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-template/send-sms"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
