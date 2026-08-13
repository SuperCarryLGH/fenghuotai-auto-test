import pytest
from config import ADMIN_URL


class TestUserProfileUpdate:
    """修改用户个人信息"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="会篡改共享 admin 账号资料，暂不执行")
    def test_UserProfileUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/profile/update"
        body = {"id": 1, "nickname": f"更新用户_194199", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
