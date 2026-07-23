import pytest
from config import ADMIN_URL


class TestRiskUserLimitDelete:
    """删除用户黑白名单"""

    @pytest.mark.smoke
    def test_RiskUserLimitDelete(self, api_session, auth_headers, autotest_user_limit_id, ok):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/delete"
        params = {"id": autotest_user_limit_id}
        ok(api_session.delete(url, params=params, headers=auth_headers))
