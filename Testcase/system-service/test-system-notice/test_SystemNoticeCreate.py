import pytest
from config import ADMIN_URL


class TestSystemNoticeCreate:
    """创建通知公告"""

    @pytest.mark.smoke
    def test_SystemNoticeCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notice/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"title": f"测试公告_194199", "content": f"测试内容_194199", "status": 0}
        # resp = api_session.post(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
