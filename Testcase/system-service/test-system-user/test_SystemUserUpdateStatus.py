import pytest
from config import ADMIN_URL


class TestSystemUserUpdateStatus:
    """修改用户状态"""

    @pytest.mark.smoke
    def test_SystemUserUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/update-status"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": "id"}  # 来自 conftest fixture
        # resp = api_session.put(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
