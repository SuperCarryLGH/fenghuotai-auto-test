import pytest
from config import ADMIN_URL


class TestStatisticsMemberUserCountComparison:
    """获得用户数量对照"""

    @pytest.mark.smoke
    def test_StatisticsMemberUserCountComparison(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/member/user-count-comparison"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
