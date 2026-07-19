import pytest
from config import ADMIN_URL


class TestSystemTenantCreate:
    """创建租户"""

    @pytest.mark.smoke
    def test_SystemTenantCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/tenant/create"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"name": f"租户_194199", "code": f"TNT_194199", "status": 0}
        # resp = api_session.post(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
