import pytest
from config import ADMIN_URL


class TestSystemTenantUpdate:
    """更新租户"""

    @pytest.mark.smoke
    def test_SystemTenantUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/tenant/update"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": "id"}  # 来自 conftest fixture
        # resp = api_session.put(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
