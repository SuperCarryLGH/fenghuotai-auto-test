import pytest
from config import ADMIN_URL


class TestSystemUserUpdateStatus:
    """修改用户状态"""

    @pytest.mark.smoke
    def test_SystemUserUpdateStatus(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update-status"
        body = {"id": autotest_user_id, "status": 0}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
