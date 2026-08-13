import pytest
import time
from config import ADMIN_URL


class TestSystemBannerCreate:
    """创建 Banner"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/banner/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_SystemBannerCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/banner/create"
        body = {"title": f"测试Banner_{int(time.time() * 1000)}",
                "picUrl": "https://example.com/banner.png",
                "position": "1", "linkType": "1", "openType": "10", "url": "https://example.com",
                "platform": "web", "provider": "all", "browseCount": 0, "memo": "autotest", "status": "0"}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
