import pytest
from config import ADMIN_URL


class TestRiskElectronicFenceDisable:
    """禁用电子围栏"""

    @pytest.mark.smoke
    def test_RiskElectronicFenceDisable(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/disable"
        body = {
            "id":2071771759382491138
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        print(r)
