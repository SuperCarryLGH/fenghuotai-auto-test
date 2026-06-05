import pytest
from Common.login import Login
from Common.loader import load_common

common = load_common()


class TestAppSmsLogin:
    """APP - 短信验证码登录"""

    @pytest.mark.smoke
    def test_app_sms_login(self, api_session):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        login = Login(session=api_session)
        token = login.app_login()

        assert token is not None
        assert len(token) > 0
        print(f"\n【提取的 token】{token}")
