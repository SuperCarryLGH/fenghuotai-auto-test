import pytest
from config import APP_URL


class TestMemberAuthSendSmsCode:
    """发送手机验证码"""

    @pytest.mark.smoke
    def test_MemberAuthSendSmsCode(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/send-sms-code"
        body = {
            "id": 1,  # TODO: 补充参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
