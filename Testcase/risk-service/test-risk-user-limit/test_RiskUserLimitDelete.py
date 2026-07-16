import pytest
from config import ADMIN_URL


class TestRiskUserLimitDelete:
    """删除用户黑白名单"""

    @pytest.mark.smoke
    def test_RiskUserLimitDelete(self, api_session, auth_headers, user_limit_id):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/delete"
        params = {"id": user_limit_id}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
