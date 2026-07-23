import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressGet:
    """获得用户收件地址"""

    @pytest.mark.smoke
    def test_MemberAddressGet(self, api_session, login_tool, autotest_address_id, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/address/get"
        params = {"id": autotest_address_id}
        ok(api_session.get(url, params=params, headers=headers))
