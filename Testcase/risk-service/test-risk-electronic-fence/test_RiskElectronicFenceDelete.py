import pytest
from config import ADMIN_URL


@pytest.mark.skip(reason="待补有效围栏ID")
class TestRiskElectronicFenceDelete:
    """删除风控-电子围栏主"""

    @pytest.mark.smoke
    def test_RiskElectronicFenceDelete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/delete"
        params = {
            "id":9999999999
        }
        ok(api_session.delete(url, params=params, headers=auth_headers))
