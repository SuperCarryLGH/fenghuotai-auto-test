import pytest
from config import APP_URL
from Common.loader import load_users, load_common
users = load_users()
common = load_common()

class TestAppApiCooperationGetByPlatform:
    """用户 APP - 发送手机验证码 Request VO"""

    @pytest.mark.smoke
    def test_AppApiCooperationGetByPlatform(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/cooperation/getByPlatform"
        params = {
            "platform": "1",
            "channel":" "
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform