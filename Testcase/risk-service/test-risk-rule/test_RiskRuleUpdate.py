import pytest
from config import ADMIN_URL


class TestRiskRuleUpdate:
    """更新风控-规则主"""

    @pytest.mark.smoke
    def test_RiskRuleUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule/update"
        body = {
              "id": 999999900,
              "ruleName": "autotest",
              "ruleCode": "",
              #"weightThreshold": 0,
              "status": 0,
              "remark": "你说的对",
              "ruleDetails": [
                {
                  "id": 62280,
                  "ruleId": 6224,
                  "minCount": 20999,
                  "maxCount": 16972,
                  "actionType": 2,
                  "actionName": "拒绝订单",
                  "sort": 0,
                  "createTime": ""
                }
              ]
            }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
