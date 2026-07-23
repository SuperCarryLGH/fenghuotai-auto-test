import pytest
from config import APP_URL
from Common.login import Login


class TestMemberUserGetCertificates:
    """获得用户证书"""

    @pytest.mark.smoke
    def test_MemberUserGetCertificates(self, api_session, login_tool, ok):
        token = login_tool.app_login(mobile="15617637160")
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/member/user/get-certificates"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
