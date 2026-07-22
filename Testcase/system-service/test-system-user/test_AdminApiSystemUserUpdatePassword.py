import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_user

common = load_common()
user_data = load_system_user()


class Test_AdminApiSystemUserUpdatePassword:
    """重置用户密码"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserUpdatePassword(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/update-password"
        body = {"id": common['common']['id']['valid'], "password": "autotest123"}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
