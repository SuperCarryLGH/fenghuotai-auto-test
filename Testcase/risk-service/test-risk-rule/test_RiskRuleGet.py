import pytest
from config import ADMIN_URL


class TestRiskRuleGet:
    """获得风控-规则主"""

    @pytest.mark.smoke
    def test_RiskRuleGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/rule/get"
        params = {
            "id":999999900
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
