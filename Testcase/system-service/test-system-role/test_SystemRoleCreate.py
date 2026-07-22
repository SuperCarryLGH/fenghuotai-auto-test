import pytest
from config import ADMIN_URL


class TestSystemRoleCreate:
    """创建角色"""

    @pytest.mark.smoke
    def test_SystemRoleCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/role/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"name": f"测试角色_194199", "code": f"AUTOTEST_194199", "sort": 0, "status": 0}
        # resp = api_session.post(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
