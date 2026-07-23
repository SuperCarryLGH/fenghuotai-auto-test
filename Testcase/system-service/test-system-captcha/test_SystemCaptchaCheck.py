import pytest
from config import ADMIN_URL


class TestSystemCaptchaCheck:
    """校验验证码"""

    @pytest.mark.smoke
    def test_SystemCaptchaCheck(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/captcha/check"
        body = {}  # TODO: 补充参数
        ok(api_session.post(url, json=body, headers=auth_headers))
        #assert r["code"] == 0
        print(r)
