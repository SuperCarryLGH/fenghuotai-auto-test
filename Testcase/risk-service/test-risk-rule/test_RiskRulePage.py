import pytest
from config import ADMIN_URL


class TestRiskRulePage:
    """获得风控-规则主分页"""

    @pytest.mark.smoke
    def test_RiskRulePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule/page"
        params = {
            "pageNo":1,
            "pageSize":10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
