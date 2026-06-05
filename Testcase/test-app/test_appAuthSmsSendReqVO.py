import pytest
from config import APP_URL
from Common.loader import load_users, load_common
users = load_users()
common = load_common()

class TestAppAuthSmsSendReqVO:
    """用户 APP - 发送手机验证码 Request VO"""

    @pytest.mark.smoke
    def test_appAuthSmsSendReqVO(self, api_session):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/member/auth/send-sms-code"
        params = {
                    "mobile": users["users"]["normal_user"]["mobile"],
                    "scene": 1
            }

        resp = api_session.post(url, json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] == {}
        print(r)