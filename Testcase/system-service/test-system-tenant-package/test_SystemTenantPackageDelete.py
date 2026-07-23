import pytest
from config import ADMIN_URL


class TestSystemTenantPackageDelete:
    """删除租户套餐"""

    @pytest.mark.smoke
    def test_SystemTenantPackageDelete(self, api_session, auth_headers, autotest_tenant_package_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/delete"
        params = {"id": autotest_tenant_package_id}
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
