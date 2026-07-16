import pytest
from config import ADMIN_URL


class TestCrmStatisticsCustomerGetCustomerSummaryByDate:
    """获取客户总量分析(按日期)"""

    @pytest.mark.smoke
    def test_CrmStatisticsCustomerGetCustomerSummaryByDate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-customer/get-customer-summary-by-date"
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
