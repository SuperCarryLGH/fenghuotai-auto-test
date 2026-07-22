import pytest
from config import ADMIN_URL


class TestRiskElectronicFenceBatchUpdate:
    """批量编辑电子围栏"""

    @pytest.mark.smoke
    def test_RiskElectronicFenceBatchUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/batch-update"
        body = {
              "ids": [9999999998],
              "ruleId": 0,
              "recyclePrice": 0,
              "clearPrice": 0,
              "status": 0
            }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
