import pytest
from config import ADMIN_URL


class TestSystemUserGetappuser:
    """获得APP用户详情"""

    @pytest.mark.smoke
    def test_SystemUserGetappuser(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/getAppUser"
        params = {"id": autotest_user_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
