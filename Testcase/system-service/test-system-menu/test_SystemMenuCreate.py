import pytest
from config import ADMIN_URL


class TestSystemMenuCreate:
    """创建菜单"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/menu/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")


    @pytest.mark.smoke
    def test_SystemMenuCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/menu/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        import time
        body = {"name": f"测试菜单_{int(time.time())}", "parentId": 100, "type": 1, "sort": 10, "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
