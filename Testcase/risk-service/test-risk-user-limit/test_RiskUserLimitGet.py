import pytest
from config import ADMIN_URL


class TestRiskUserLimitGet:
    """获得风控-访问控制名单(黑白名单)"""

    @pytest.mark.smoke
    def test_RiskUserLimitGet(self, api_session, auth_headers, autotest_user_limit_id, ok):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/get"
        params = {"id": autotest_user_limit_id}
        ok(api_session.get(url, params=params, headers=auth_headers))
