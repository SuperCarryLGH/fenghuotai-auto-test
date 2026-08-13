import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemUserUpdateStatus:
    """修改用户状态"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserUpdateStatus(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update-status"
        body = {"id": autotest_user_id, "status": 0}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
