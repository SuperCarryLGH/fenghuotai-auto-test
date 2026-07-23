import pytest
from config import ADMIN_URL


class TestStatisticsTradeSummary:
    """获得交易统计"""

    @pytest.mark.smoke
    def test_StatisticsTradeSummary(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/summary"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
