import pytest
from config import ADMIN_URL


class TestSystemMenuGet:
    """获取菜单信息"""

    @pytest.mark.smoke
    def test_SystemMenuGet(self, api_session, auth_headers, autotest_menu_id):
        url = f"{ADMIN_URL}/admin-api/system/menu/get"
        params = {"id": autotest_menu_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
