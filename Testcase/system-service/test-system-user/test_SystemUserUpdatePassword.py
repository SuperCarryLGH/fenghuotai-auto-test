import pytest
from config import ADMIN_URL


class TestSystemUserUpdatePassword:
    """重置用户密码"""

    @pytest.mark.smoke
    def test_SystemUserUpdatePassword(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update-password"
        body = {"id": autotest_user_id, "password": "autotest123"}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
