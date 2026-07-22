import pytest
from config import ADMIN_URL


class TestRiskElectronicFenceGet:
    """获得风控-电子围栏主"""

    @pytest.mark.smoke
    def test_RiskElectronicFenceGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/get"
        params = {
            "id":999999,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
