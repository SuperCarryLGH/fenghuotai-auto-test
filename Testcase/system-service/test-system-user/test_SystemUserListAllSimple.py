import pytest
from config import ADMIN_URL


class TestSystemUserListAllSimple:
    """获取用户精简信息列表"""

    @pytest.mark.smoke
    def test_SystemUserListAllSimple(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/list-all-simple"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
