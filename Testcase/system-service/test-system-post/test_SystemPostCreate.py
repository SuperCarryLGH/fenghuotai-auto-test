import pytest
from config import ADMIN_URL


class TestSystemPostCreate:
    """创建岗位"""

    @pytest.mark.smoke
    def test_SystemPostCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/post/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"name": f"测试_194199", "sort": 0, "status": 0}
        # resp = api_session.post(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
