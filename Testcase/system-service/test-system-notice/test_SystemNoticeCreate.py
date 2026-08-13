import pytest
import time
from config import ADMIN_URL


class TestSystemNoticeCreate:
    """创建通知公告"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/notice/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_SystemNoticeCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notice/create"
        body = {"title": f"测试公告_{int(time.time() * 1000)}", "content": f"测试内容_{int(time.time() * 1000)}", "type": 1, "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
