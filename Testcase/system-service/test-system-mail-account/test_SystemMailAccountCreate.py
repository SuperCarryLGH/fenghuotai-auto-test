import pytest
from config import ADMIN_URL


class TestSystemMailAccountCreate:
    """创建邮箱账号"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/mail-account/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")


    @pytest.mark.smoke
    def test_SystemMailAccountCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/create"
        body = {"mail": f"test_194199@test.com", "username": f"test_194199", "password": "123456", "host": "smtp.test.com", "port": 465, "starttlsEnable": False, "sslEnable": False, "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
