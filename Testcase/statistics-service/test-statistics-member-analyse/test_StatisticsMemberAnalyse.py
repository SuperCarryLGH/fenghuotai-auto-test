import pytest
from config import ADMIN_URL


class TestStatisticsMemberAnalyse:
    """获得会员分析数据"""

    @pytest.mark.smoke
    def test_StatisticsMemberAnalyse(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/member/analyse"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
