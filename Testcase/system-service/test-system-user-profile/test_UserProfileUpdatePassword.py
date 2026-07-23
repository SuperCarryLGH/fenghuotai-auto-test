import pytest
from config import ADMIN_URL


class TestUserProfileUpdatePassword:
    """修改用户个人密码"""

    @pytest.mark.smoke
    def test_UserProfileUpdatePassword(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/profile/update-password"
        body = {
                  "oldPassword": "1qaz!QAZ",
                  "newPassword": "1qaz!QAZ"
                }  # TODO: 补充参数
        ok(api_session.put(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
