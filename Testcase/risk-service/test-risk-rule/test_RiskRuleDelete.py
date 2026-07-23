import pytest
from config import ADMIN_URL


@pytest.mark.skip(reason="待补有效规则ID")
class TestRiskRuleDelete:
    """删除风控-规则主"""

    @pytest.mark.smoke
    def test_RiskRuleDelete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/rule/delete"
        params = {
            "id":999999999
        }
        ok(api_session.delete(url, params=params, headers=auth_headers))
