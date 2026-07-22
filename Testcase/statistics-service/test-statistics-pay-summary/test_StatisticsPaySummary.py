import pytest
from config import ADMIN_URL


class TestStatisticsPaySummary:
    """获取充值金额"""

    @pytest.mark.smoke
    def test_StatisticsPaySummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/pay/summary"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
