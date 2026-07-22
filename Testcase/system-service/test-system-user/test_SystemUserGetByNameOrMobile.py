import pytest
from config import ADMIN_URL


class TestSystemUserGetByNameOrMobile:
    """根据用户姓名或者手机号查询用户信息"""

    @pytest.mark.smoke
    def test_SystemUserGetByNameOrMobile(self, api_session, auth_headers, autotest_user_id):
        url = f"{ADMIN_URL}/admin-api/system/user/get-by-name-or-mobile"
        params = {"id": autotest_user_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
