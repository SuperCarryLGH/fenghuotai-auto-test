import pytest
from config import ADMIN_URL


class TestRiskRuleDetailDelete:
    """删除风控-规则区间明细"""

    @pytest.mark.smoke
    def test_RiskRuleDetailDelete(self, api_session, auth_headers, autotest_rule_detail_id, ok):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/delete"
        params = {"id": autotest_rule_detail_id}
        ok(api_session.delete(url, params=params, headers=auth_headers))
