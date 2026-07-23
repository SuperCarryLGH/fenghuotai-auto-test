import pytest
from config import ADMIN_URL


class TestRiskElectronicFenceDeleteList:
    """批量删除风控-电子围栏主"""

    @pytest.mark.smoke
    def test_RiskElectronicFenceDeleteList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/delete-list"
        params = {
            "ids":9999999999
        }
        ok(api_session.delete(url, params=params, headers=auth_headers))
