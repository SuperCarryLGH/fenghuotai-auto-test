import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressGetDefault:
    """获得默认的用户收件地址"""

    @pytest.mark.smoke
    def test_MemberAddressGetDefault(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/address/get-default"
        params = {}
        ok(api_session.get(url, params=params, headers=headers))
