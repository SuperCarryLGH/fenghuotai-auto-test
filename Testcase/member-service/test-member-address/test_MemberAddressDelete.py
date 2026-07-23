import pytest
from config import APP_URL
from Common.login import Login


class TestMemberAddressDelete:
    """删除用户收件地址"""

    @pytest.mark.smoke
    def test_MemberAddressDelete(self, api_session, login_tool, autotest_address_id, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/address/delete"
        params = {"id": autotest_address_id}
        ok(api_session.delete(url, params=params, headers=headers))
