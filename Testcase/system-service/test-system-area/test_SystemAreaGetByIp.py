import pytest
from config import ADMIN_URL


class TestSystemAreaGetByIp:
    """获得 IP 对应的地区名"""

    @pytest.mark.smoke
    def test_SystemAreaGetByIp(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/area/get-by-ip"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
