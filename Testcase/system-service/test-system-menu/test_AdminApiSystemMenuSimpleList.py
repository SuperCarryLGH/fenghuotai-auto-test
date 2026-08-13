import pytest
from config import ADMIN_URL


class TestAdminApiSystemMenuSimpleList:
    """获取菜单精简信息列表"""

    @pytest.mark.smoke
    def test_AdminApiSystemMenuSimpleList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/menu/simple-list"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
