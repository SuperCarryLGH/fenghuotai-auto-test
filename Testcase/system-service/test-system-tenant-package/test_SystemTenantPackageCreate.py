import pytest
from config import ADMIN_URL


class TestSystemTenantPackageCreate:
    """创建租户套餐"""

    @pytest.mark.smoke
    def test_SystemTenantPackageCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        import time
        body = {"name": f"套餐_{int(time.time())}", "menuIds": [1], "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
