import pytest
from config import ADMIN_URL


class TestRiskRuleDetailUpdate:
    """更新风控-规则区间明细"""

    @pytest.mark.smoke
    def test_RiskRuleDetailUpdate(self, api_session, auth_headers, autotest_rule_detail_id, ok):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/update"
        body = {
            "id": autotest_rule_detail_id,
            "ruleId": 1,
            "minCount": 3,
            "maxCount": 5,
            "actionType": 10,
            "sort": 1,
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
