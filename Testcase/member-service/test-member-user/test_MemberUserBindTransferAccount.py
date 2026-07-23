import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserBindTransferAccount:
    """绑定转账账号"""

    @pytest.mark.smoke
    def test_MemberUserBindTransferAccount(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/bind-transfer-account"
        body = {"id": 1}  # TODO: 替换为实际 ID
        ok(api_session.post(url, json=body, headers=headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
