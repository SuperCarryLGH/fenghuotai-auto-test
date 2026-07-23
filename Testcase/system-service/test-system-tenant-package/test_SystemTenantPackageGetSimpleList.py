import pytest
from config import ADMIN_URL


class TestSystemTenantPackageGetSimpleList:
    """获取租户套餐精简信息列表"""

    @pytest.mark.smoke
    def test_SystemTenantPackageGetSimpleList(self, api_session, auth_headers, autotest_tenant_package_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/tenant-package/get-simple-list"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {
            # TODO: 核对参数后取消下方注释
        }
        ok(api_session.get(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
