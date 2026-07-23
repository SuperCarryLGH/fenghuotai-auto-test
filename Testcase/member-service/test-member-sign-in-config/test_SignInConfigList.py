import pytest
from config import ADMIN_URL


class TestSignInConfigList:
    """获得签到规则列表"""

    @pytest.mark.smoke
    def test_SignInConfigList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
