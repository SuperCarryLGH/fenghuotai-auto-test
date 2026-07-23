import pytest
from config import ADMIN_URL


class TestSystemTenantPackagePage:
    """获得租户套餐分页"""

    @pytest.mark.smoke
    def test_SystemTenantPackagePage(self, api_session, auth_headers, autotest_tenant_package_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/page"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        ok(api_session.get(url, json=body, headers=auth_headers))
