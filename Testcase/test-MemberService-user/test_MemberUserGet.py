import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserGet:
    """获得会员用户"""

    @pytest.mark.smoke
    def test_MemberUserGet(self, api_session,login_tool):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        mobile = "15617617160"
        token = login_tool.app_login(mobile=mobile)
        print(token)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/get-certificates"
        params = {
            #"id": 1 #编号
            }

        resp = api_session.get(url, headers=headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform