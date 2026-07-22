import pytest
from config import ADMIN_URL


class TestStatisticsMemberSummary:
    """获得会员统计（实时统计）"""

    @pytest.mark.smoke
    def test_StatisticsMemberSummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/member/summary"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
