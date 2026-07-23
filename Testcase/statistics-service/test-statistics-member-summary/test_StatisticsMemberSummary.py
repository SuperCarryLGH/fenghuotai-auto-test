import pytest
from config import ADMIN_URL


class TestStatisticsMemberSummary:
    """获得会员统计（实时统计）"""

    @pytest.mark.smoke
    def test_StatisticsMemberSummary(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/member/summary"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
