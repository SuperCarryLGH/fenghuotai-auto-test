import pytest
from config import ADMIN_URL


class TestRiskRuleDelete:
    """删除风控-规则主"""

    @pytest.mark.smoke
    def test_RiskRuleDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule/delete"
        params = {
            "id":999999999
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
