import time
import pytest
from config import ADMIN_URL


class TestSignInConfigCreate:
    """创建签到规则"""

    @pytest.mark.smoke
    def test_SignInConfigCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/create"
        body = {"day": int(time.time()) % 365 + 1, "point": 10, "experience": 10, "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
