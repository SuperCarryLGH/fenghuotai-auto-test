import pytest
from config import ADMIN_URL


class TestSystemUserSimpleList:
    """获取用户精简信息列表"""

    @pytest.mark.smoke
    def test_SystemUserSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
