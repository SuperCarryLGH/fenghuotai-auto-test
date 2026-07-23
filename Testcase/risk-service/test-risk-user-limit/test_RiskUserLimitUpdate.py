import pytest
from config import ADMIN_URL


class TestRiskUserLimitUpdate:
    """修改用户黑白名单"""

    @pytest.mark.smoke
    def test_RiskUserLimitUpdate(self, api_session, auth_headers, autotest_user_limit_id, ok):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/update"
        body = {
            "id": autotest_user_limit_id,
            "reason": "autotest_updated",
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
