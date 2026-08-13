import pytest
from config import ADMIN_URL


class TestSystemAreaGetByIp:
    """获得 IP 对应的地区名"""

    @pytest.mark.smoke
    def test_SystemAreaGetByIp(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/area/get-by-ip"
        params = {"ip": "123.160.230.187"}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
