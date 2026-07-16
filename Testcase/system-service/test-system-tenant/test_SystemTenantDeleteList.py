import pytest
from config import ADMIN_URL


class TestSystemTenantDeleteList:
    """批量删除租户"""

    @pytest.mark.smoke
    def test_SystemTenantDeleteList(self, api_session, auth_headers, system_tenant_id):
        url = f"{ADMIN_URL}/admin-api/system/tenant/delete-list"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"ids": str(autotest_tenant_id)}  # 来自 conftest fixture
        # resp = api_session.delete(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
