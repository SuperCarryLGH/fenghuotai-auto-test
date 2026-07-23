import pytest
from config import ADMIN_URL


class TestStatisticsMemberTerminalStatisticsList:
    """按照终端，获得会员统计列表"""

    @pytest.mark.smoke
    def test_StatisticsMemberTerminalStatisticsList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/member/terminal-statistics-list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
