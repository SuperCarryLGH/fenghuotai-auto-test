import time
import pytest
from config import ADMIN_URL


class TestSignInConfigCreate:
    """创建签到规则"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/member/sign-in/config/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_SignInConfigCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/create"
        day = int(time.time()) % 365 + 1
        # 幂等：先删该 day 旧配置，避免跨运行残留导致 1004009001(已存在)
        lst = api_session.get(f"{ADMIN_URL}/admin-api/member/sign-in/config/list",
                              headers=auth_headers).json().get("data") or []
        for item in lst:
            if str(item.get("day")) == str(day):
                api_session.delete(f"{ADMIN_URL}/admin-api/member/sign-in/config/delete",
                                   params={"id": item["id"]}, headers=auth_headers)
        body = {"day": day, "point": 10, "experience": 10, "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
