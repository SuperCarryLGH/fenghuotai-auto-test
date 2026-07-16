import pytest
from config import ADMIN_URL


class TestSystemAuthResetPassword:
    """重置密码"""

    @pytest.mark.smoke
    def test_SystemAuthResetPassword(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/reset-password"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
