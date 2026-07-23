import pytest
from config import ADMIN_URL


class TestRiskUserLimitPage:
    """分页查询用户黑白名单"""

    @pytest.mark.smoke
    def test_RiskUserLimitPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
            "type": 1,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
