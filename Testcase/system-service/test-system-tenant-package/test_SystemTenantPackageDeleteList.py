import pytest
from config import ADMIN_URL


class TestSystemTenantPackageDeleteList:
    """批量删除租户套餐"""

    @pytest.mark.smoke
    def test_SystemTenantPackageDeleteList(self, api_session, auth_headers, autotest_tenant_package_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/delete-list"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        params = {"ids": [autotest_tenant_package_id]}
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
