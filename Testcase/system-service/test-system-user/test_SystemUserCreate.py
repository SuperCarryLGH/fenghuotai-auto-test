import pytest
from config import ADMIN_URL


class TestSystemUserCreate:
    """新增用户"""

    @pytest.mark.smoke
    def test_SystemUserCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/create"
        import time
        suffix = str(int(time.time()))[-8:]
        body = {"username": f"test{suffix}", "password": "123456", "nickname": f"用户{suffix}", "mobile": f"156{suffix}", "sex": 1, "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
