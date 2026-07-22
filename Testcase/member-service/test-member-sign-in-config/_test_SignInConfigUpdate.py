import pytest
from config import ADMIN_URL


class TestSignInConfigUpdate:
    """更新签到规则"""

    @pytest.mark.smoke
    def test_SignInConfigUpdate(self, api_session, auth_headers, autotest_config_id):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/update"
        body = {"id": autotest_config_id, "day": 1, "point": 20, "experience": 20, "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
