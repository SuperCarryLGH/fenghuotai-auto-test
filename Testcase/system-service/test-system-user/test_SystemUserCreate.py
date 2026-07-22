import pytest
from config import ADMIN_URL


class TestSystemUserCreate:
    """新增用户"""

    @pytest.mark.smoke
    def test_SystemUserCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/create"
        import time
        suffix = str(int(time.time()))[-8:]
        body = {"username": f"test{suffix}", "password": "123456", "nickname": f"用户{suffix}", "mobile": f"156{suffix}", "sex": 1, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
