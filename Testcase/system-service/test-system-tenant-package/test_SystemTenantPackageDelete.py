import pytest
from config import ADMIN_URL


class TestSystemTenantPackageDelete:
    """删除租户套餐"""

    @pytest.mark.smoke
    def test_SystemTenantPackageDelete(self, api_session, auth_headers, autotest_tenant_package_id):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/delete"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        resp = api_session.delete(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
