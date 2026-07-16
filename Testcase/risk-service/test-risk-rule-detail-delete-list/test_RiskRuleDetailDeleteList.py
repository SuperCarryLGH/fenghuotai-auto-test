import pytest
from config import ADMIN_URL


class TestRiskRuleDetailDeleteList:
    """批量删除风控-规则区间明细"""

    @pytest.mark.smoke
    def test_RiskRuleDetailDeleteList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/delete-list"
        params = {
            "ids":2072920935440969729
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
