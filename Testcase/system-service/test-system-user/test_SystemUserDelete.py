import pytest
from config import ADMIN_URL


class TestSystemUserDelete:
    """删除用户"""

    @pytest.mark.smoke
    def test_SystemUserDelete(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/delete"
        params = {"id": autotest_user_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
