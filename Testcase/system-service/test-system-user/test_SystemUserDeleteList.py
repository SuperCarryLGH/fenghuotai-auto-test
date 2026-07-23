import pytest
from config import ADMIN_URL


class TestSystemUserDeleteList:
    """批量删除用户"""

    @pytest.mark.smoke
    def test_SystemUserDeleteList(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/delete-list"
        params = {"ids": str(autotest_user_id)}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
