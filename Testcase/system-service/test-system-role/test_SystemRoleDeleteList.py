import pytest
from config import ADMIN_URL


class TestSystemRoleDeleteList:
    """批量删除角色"""

    @pytest.mark.smoke
    def test_SystemRoleDeleteList(self, api_session, auth_headers, system_role_id):
        url = f"{ADMIN_URL}/admin-api/system/role/delete-list"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"ids": str(autotest_role_id)}  # 来自 conftest fixture
        # resp = api_session.delete(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
