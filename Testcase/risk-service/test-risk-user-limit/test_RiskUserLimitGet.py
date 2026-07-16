import pytest
from config import ADMIN_URL


class TestRiskUserLimitGet:
    """获得风控-访问控制名单(黑白名单)"""

    @pytest.mark.smoke
    def test_RiskUserLimitGet(self, api_session, auth_headers, user_limit_id):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/get"
        params = {"id": user_limit_id}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
