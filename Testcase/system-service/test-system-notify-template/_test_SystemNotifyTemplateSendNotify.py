import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateSendNotify:
    """发送站内信"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateSendNotify(self, api_session, auth_headers, autotest_notify_template_id):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/send-notify"
        body = {"userId": 1, "userType": 1, "templateCode": "NTF_194199"}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
