import pytest
from config import APP_URL


class TestMemberAuthValidateSmsCode:
    """校验手机验证码"""

    @pytest.mark.smoke
    def test_MemberAuthValidateSmsCode(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/validate-sms-code"
        body = {
            # TODO: 补充请求体参数
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
