import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressList:
    """获得用户收件地址列表"""

    @pytest.mark.smoke
    def test_MemberAddressList(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/address/list"
        params = {"pageNo": 1, "pageSize": 10}
        ok(api_session.get(url, params=params, headers=headers))
