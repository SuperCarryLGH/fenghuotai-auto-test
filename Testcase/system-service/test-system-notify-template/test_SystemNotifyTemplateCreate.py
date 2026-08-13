import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateCreate:
    """创建站内信模版"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/notify-template/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")


    @pytest.mark.smoke
    def test_SystemNotifyTemplateCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/create"
        import time
        body = {"name": f"通知模板_{int(time.time())}", "code": f"NTF_{int(time.time())}", "content": "测试内容", "type": 1, "nickname": "autotest", "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
