import pytest
from config import ADMIN_URL


class TestSystemMenuGet:
    """获取菜单信息"""

    @pytest.mark.smoke
    def test_SystemMenuGet(self, api_session, auth_headers, autotest_menu_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/menu/get"
        params = {"id": autotest_menu_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
