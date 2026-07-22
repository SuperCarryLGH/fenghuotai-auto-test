import pytest
from config import ADMIN_URL


class TestRiskElectronicFencePage:
    """获得风控-电子围栏主分页（包含规则信息）"""

    @pytest.mark.smoke
    def test_RiskElectronicFencePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
