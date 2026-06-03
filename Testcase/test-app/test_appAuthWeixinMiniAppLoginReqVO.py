import pytest
from Common.login import Login


class TestAppWeixinMiniAppLogin:
    """APP - 微信小程序手机号登录"""

    @pytest.mark.smoke
    def test_weixin_mini_app_login(self, api_session):
        """
        微信小程序手机号登录
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        login = Login(session=api_session)
        token = login.app_login(
            phone_code="test_phone_code",
            login_code="test_login_code",
        )

        assert token is not None
        assert len(token) > 0
        print(f"\n【提取的 token】{token}")
