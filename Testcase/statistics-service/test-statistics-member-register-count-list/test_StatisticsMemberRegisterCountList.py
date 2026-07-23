import pytest
from config import ADMIN_URL


class TestStatisticsMemberRegisterCountList:
    """获得会员注册数量列表"""

    @pytest.mark.smoke
    def test_StatisticsMemberRegisterCountList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/member/register-count-list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
