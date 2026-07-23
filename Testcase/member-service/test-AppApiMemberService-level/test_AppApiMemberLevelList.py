import pytest
from config import APP_URL
from Common.login import Login

class TestAppApiMemberLevelList:
    """获得会员等级列表"""

    @pytest.mark.smoke
    def test_TestAppApiMemberLevelList(self,api_session,login_tool, ok):
        mobile = "18600000000"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/app-api/member/level/list"
        params = {
            #"": ""
            }

        ok(api_session.get(url, params=params, headers=headers))
