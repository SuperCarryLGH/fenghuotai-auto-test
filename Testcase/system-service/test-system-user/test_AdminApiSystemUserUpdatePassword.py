import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_user

common = load_common()
user_data = load_system_user()


class Test_AdminApiSystemUserUpdatePassword:
    """重置用户密码"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserUpdatePassword(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update-password"
        body = {"id": autotest_user_id, "password": "autotest123"}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
