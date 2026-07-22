import pytest
from config import ADMIN_URL


class TestRiskRuleCreate:
    """创建风控-规则主"""

    @pytest.mark.smoke
    def test_RiskRuleCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/rule/create"
        body = {
              "id": 999999999,
              "ruleName": "autotest",
              "ruleCode": "",
              #"weightThreshold": 0,
              "status": 0,
              "remark": "autotest",
              "ruleDetails": [
                {
                  "id": 28660,
                  "ruleId": 622800,
                  "minCount": 20999,
                  "maxCount": 16972,
                  "actionType": 2,
                  "actionName": "拒绝订单",
                  "sort": 0,
                  "createTime": ""
                }
              ]
            }
        resp = api_session.post(url, json=body, headers=auth_headers)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        print(r)
