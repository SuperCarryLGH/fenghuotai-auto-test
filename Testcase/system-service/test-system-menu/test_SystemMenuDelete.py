import pytest
from config import ADMIN_URL


class TestSystemMenuDelete:
    """删除菜单"""

    @pytest.mark.smoke
    def test_SystemMenuDelete(self, api_session, auth_headers, autotest_menu_id):
        url = f"{ADMIN_URL}/admin-api/system/menu/delete"
        params = {"id": autotest_menu_id}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
