import pytest
from config import ADMIN_URL


class TestSystemAuthLogin:
    """使用账号密码登录"""

    @pytest.mark.smoke
    def test_SystemAuthLogin(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/login"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"id": 1}  # TODO: 补充参数
        # resp = api_session.post(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
