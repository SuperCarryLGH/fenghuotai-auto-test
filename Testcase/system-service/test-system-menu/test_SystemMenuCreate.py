import pytest
from config import ADMIN_URL


class TestSystemMenuCreate:
    """创建菜单"""

    @pytest.mark.smoke
    def test_SystemMenuCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/menu/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        import time
        body = {"name": f"测试菜单_{int(time.time())}", "parentId": 100, "type": 1, "sort": 0, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
