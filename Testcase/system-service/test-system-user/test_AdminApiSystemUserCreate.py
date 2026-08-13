import time
import pytest
from config import ADMIN_URL


class TestCreateUser:
    """新增用户"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/user/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

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

        r = ok(api_session.post(url, json=payload, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
