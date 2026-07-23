import pytest
from config import ADMIN_URL


class TestUserProfileGet:
    """获得登录用户信息"""

    @pytest.mark.smoke
    def test_UserProfileGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/profile/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
