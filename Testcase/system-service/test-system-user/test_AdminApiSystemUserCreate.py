import time
import pytest
from config import ADMIN_URL


class TestCreateUser:
    """新增用户"""

    @pytest.mark.smoke
    def test_create_user(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/create"
        suffix = str(int(time.time()))[-8:]
        payload = {
            "username": f"user{suffix}",
            "password": "autotest123",
            "nickname": "西音",
            "mobile": f"156{suffix}",
            "sex": 1,
            "status": 0,
        }

        ok(api_session.post(url, json=payload, headers=auth_headers))
        data = resp.json()
        assert data["code"] == 0
