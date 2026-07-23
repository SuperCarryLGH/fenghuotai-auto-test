import pytest
from config import ADMIN_URL


class TestSystemMenuDelete:
    """删除菜单"""

    @pytest.mark.smoke
    def test_SystemMenuDelete(self, api_session, auth_headers, autotest_menu_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/menu/delete"
        params = {"id": autotest_menu_id}
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
