import pytest
from config import ADMIN_URL


class TestRiskUserLimitCreate:
    """新增用户黑白名单"""

    @pytest.mark.smoke
    def test_RiskUserLimitCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/user-limit/create"
        body = {
              "id": 16666666666,
              "type": 2,
              "targetType": 1,
              "targetId": "16666666666",
              "reason": "违规操作",
              "periodType": 0,
              "effectiveTime": "",
              "expireTime": "",
              "status": 0
            }
        ok(api_session.post(url, json=body, headers=auth_headers))
