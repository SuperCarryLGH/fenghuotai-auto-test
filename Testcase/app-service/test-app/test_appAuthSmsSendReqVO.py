import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_users, load_common
users = load_users()
common = load_common()

@pytest.mark.skip(reason="超过每日短信发送数量，待明日重试")
class TestAppAuthSmsSendReqVO:
    """发送手机验证码"""

    @pytest.mark.smoke
    def test_appAuthSmsSendReqVO(self, api_session, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/member/auth/send-sms-code"
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000))}
        params = {
                    "mobile": users["users"]["normal_user"]["mobile"],
                    "scene": 1
            }

        ok(api_session.post(url, json=params, headers=headers))