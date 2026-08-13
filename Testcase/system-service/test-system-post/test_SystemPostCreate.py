import pytest
import time
from config import ADMIN_URL


class TestSystemPostCreate:
    """创建岗位"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/post/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_SystemPostCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/create"
        body = {"name": f"测试_194199", "code": f"TEST_POST_{int(time.time() * 1000)}", "sort": 0, "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
