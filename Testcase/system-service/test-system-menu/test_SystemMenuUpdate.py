import pytest
from config import ADMIN_URL


class TestSystemMenuUpdate:
    """修改菜单"""

    @pytest.mark.smoke
    def test_SystemMenuUpdate(self, api_session, auth_headers, autotest_menu_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/menu/update"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": autotest_menu_id, "name": "autotest_updated", "type": 1, "sort": 0, "parentId": 100, "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
