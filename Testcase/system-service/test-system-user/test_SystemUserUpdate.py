import pytest
from config import ADMIN_URL


class TestSystemUserUpdate:
    """修改用户"""

    @pytest.mark.smoke
    def test_SystemUserUpdate(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update"
        suffix = str(autotest_user_id)[-8:]
        body = {
            "id": autotest_user_id,
            "username": f"upd{suffix}",
            "nickname": "更新用户_autotest",
            "mobile": f"186{suffix}",
            "sex": 1,
            "status": 0,
        }
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
