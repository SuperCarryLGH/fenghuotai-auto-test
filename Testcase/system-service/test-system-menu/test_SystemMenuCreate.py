import pytest
from config import ADMIN_URL


class TestSystemMenuCreate:
    """创建菜单"""

    @pytest.mark.smoke
    def test_SystemMenuCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/menu/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        import time
        body = {"name": f"测试菜单_{int(time.time())}", "parentId": 100, "type": 1, "sort": 0, "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
