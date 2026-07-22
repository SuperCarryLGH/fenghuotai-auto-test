import pytest
from config import ADMIN_URL


class TestSmsCallbackTencent:
    """腾讯云短信的回调"""

    @pytest.mark.smoke
    def test_SmsCallbackTencent(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms/callback/tencent"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
