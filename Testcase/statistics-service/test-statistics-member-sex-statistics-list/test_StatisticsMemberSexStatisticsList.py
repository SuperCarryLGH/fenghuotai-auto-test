import pytest
from config import ADMIN_URL


class TestStatisticsMemberSexStatisticsList:
    """按照性别，获得会员统计列表"""

    @pytest.mark.smoke
    def test_StatisticsMemberSexStatisticsList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/statistics/member/sex-statistics-list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
