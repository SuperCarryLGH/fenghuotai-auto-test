import pytest
from config import ADMIN_URL


class TestSystemTenantPackageUpdate:
    """更新租户套餐"""

    @pytest.mark.smoke
    def test_SystemTenantPackageUpdate(self, api_session, auth_headers, autotest_tenant_package_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/update"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": autotest_tenant_package_id, "name": "autotest_updated", "menuIds": [1], "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
