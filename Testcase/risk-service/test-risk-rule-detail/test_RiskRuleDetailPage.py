import pytest
from config import ADMIN_URL


class TestRiskRuleDetailPage:
    """获得风控-规则区间明细分页"""

    @pytest.mark.smoke
    def test_RiskRuleDetailPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/rule-detail/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
