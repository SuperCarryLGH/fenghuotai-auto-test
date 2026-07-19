import pytest
from config import ADMIN_URL


class TestRiskRuleDetailGet:
    """获得风控-规则区间明细"""

    @pytest.mark.smoke
    def test_RiskRuleDetailGet(self, api_session, auth_headers, autotest_rule_detail_id):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/get"
        params = {"id": autotest_rule_detail_id}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
