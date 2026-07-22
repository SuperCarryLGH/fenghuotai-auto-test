import pytest
from config import ADMIN_URL


class TestCrmStatisticsFunnelGetBusinessInversionRateSummaryByDate:
    """获取商机转化率分析(按日期)"""

    @pytest.mark.smoke
    def test_CrmStatisticsFunnelGetBusinessInversionRateSummaryByDate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-funnel/get-business-inversion-rate-summary-by-date"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
