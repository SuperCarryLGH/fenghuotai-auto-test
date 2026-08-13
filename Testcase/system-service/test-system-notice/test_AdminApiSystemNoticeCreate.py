import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_notice

common = load_common()
notice_data = load_system_notice()


class Test_AdminApiSystemNoticeCreate:
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
    def test_AdminApiSystemNoticeCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notice/create"
        suffix = str(int(time.time()))
        body = {
            "title": f"{notice_data['notice']['name']}_{suffix}",
            "content": f"测试公告内容_{suffix}",
            "type": 1,
            "status": 0,
        }
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
