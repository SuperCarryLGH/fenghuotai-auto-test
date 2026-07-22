import pytest
from config import ADMIN_URL


class TestSystemMenuListAllSimple:
    """获取菜单精简信息列表"""

    @pytest.mark.smoke
    def test_SystemMenuListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/menu/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
