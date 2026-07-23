import pytest
from config import ADMIN_URL


class TestSystemTenantPackageGet:
    """获得租户套餐"""

    @pytest.mark.smoke
    def test_SystemTenantPackageGet(self, api_session, auth_headers, autotest_tenant_package_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/get"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        params = {"id": autotest_tenant_package_id}
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
