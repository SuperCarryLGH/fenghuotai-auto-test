import pytest
from config import ADMIN_URL


class TestSystemAreaTree:
    """获得地区树"""

    @pytest.mark.smoke
    def test_SystemAreaTree(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/area/tree"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=auth_headers))
