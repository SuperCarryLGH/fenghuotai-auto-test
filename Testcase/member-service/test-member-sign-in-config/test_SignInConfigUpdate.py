import pytest
from config import ADMIN_URL


class TestSignInConfigUpdate:
    """更新签到规则"""

    @pytest.mark.smoke
    def test_SignInConfigUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/update"
        body = {"id": "member_sign_in_config_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
