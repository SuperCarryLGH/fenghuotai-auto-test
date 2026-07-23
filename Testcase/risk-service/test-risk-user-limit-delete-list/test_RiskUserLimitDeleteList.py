import pytest
from config import ADMIN_URL


class TestRiskUserLimitDeleteList:
    """批量删除风控-访问控制名单(黑白名单)"""

    @pytest.mark.smoke
    def test_RiskUserLimitDeleteList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/delete-list"
        params = {"ids": [1666666666]}
        ok(api_session.delete(url, params=params, headers=auth_headers))