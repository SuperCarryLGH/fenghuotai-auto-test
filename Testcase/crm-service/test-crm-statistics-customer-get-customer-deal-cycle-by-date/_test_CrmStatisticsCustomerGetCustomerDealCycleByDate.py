import pytest
from config import ADMIN_URL


class TestCrmStatisticsCustomerGetCustomerDealCycleByDate:
    """获取客户成交周期(按日期)"""

    @pytest.mark.smoke
    def test_CrmStatisticsCustomerGetCustomerDealCycleByDate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-customer/get-customer-deal-cycle-by-date"
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
