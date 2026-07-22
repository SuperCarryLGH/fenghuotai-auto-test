import pytest
import time
from config import ADMIN_URL


class TestRiskRuleDetailCreate:
    """创建风控-规则区间明细"""

    @pytest.mark.smoke
    def test_RiskRuleDetailCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/create"
        ruleId = int(time.time() * 1000000)
        body = {
              #"id": 33333333,
              "ruleId": ruleId,
              "minCount": 1,
              "maxCount": 2,
              "actionType": 10,
              "sort": 0
            }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
