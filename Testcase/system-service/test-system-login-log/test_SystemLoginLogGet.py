import pytest
from config import ADMIN_URL


class TestSystemLoginLogGet:
    """获得登录日志"""

    @pytest.mark.smoke
    def test_SystemLoginLogGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/login-log/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
