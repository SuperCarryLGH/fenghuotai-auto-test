import pytest
from config import ADMIN_URL


class TestSystemUserUpdate:
    """修改用户"""

    @pytest.mark.smoke
    def test_SystemUserUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update"
        body = {"id": 1, "nickname": f"更新用户_194199", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
