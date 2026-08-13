import pytest
from config import ADMIN_URL


class TestSystemCaptchaCheck:
    """校验验证码"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="验证码接口需 uuid+code 参数，暂无有效数据")
    def test_SystemCaptchaCheck(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/captcha/check"
        body = {}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        print(r)
