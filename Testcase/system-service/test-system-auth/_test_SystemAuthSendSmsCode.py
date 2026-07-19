import pytest
from config import ADMIN_URL


class TestSystemAuthSendSmsCode:
    """发送手机验证码"""

    @pytest.mark.smoke
    def test_SystemAuthSendSmsCode(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/send-sms-code"
        body = {"mobile": 15617617160}  # TODO: 替换为实际 ID
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
