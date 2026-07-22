import pytest
from config import ADMIN_URL


class TestSignInConfigCreate:
    """创建签到规则"""

    @pytest.mark.smoke
    def test_SignInConfigCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/create"
        body = {"name": f"配置_194200", "value": f"val_194200"}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
