import pytest
from config import ADMIN_URL


class TestRiskUserLimitPage:
    """分页查询用户黑白名单"""

    @pytest.mark.smoke
    def test_RiskUserLimitPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
