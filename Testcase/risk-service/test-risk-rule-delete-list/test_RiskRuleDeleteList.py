import pytest
from config import ADMIN_URL


class TestRiskRuleDeleteList:
    """批量删除风控-规则主"""

    @pytest.mark.smoke
    def test_RiskRuleDeleteList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/rule/delete-list"
        params = {
            "ids":999999999
        }
        ok(api_session.delete(url, params=params, headers=auth_headers))
