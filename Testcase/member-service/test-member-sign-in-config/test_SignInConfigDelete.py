import pytest
from config import ADMIN_URL


class TestSignInConfigDelete:
    """删除签到规则"""

    @pytest.mark.smoke
    def test_SignInConfigDelete(self, api_session, auth_headers, autotest_config_id, ok):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/delete"
        params = {"id": autotest_config_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
