import pytest
from config import ADMIN_URL


class TestCrmStatisticsCustomerGetCustomerDealCycleByProduct:
    """获取客户成交周期(按用户)"""

    @pytest.mark.smoke
    def test_CrmStatisticsCustomerGetCustomerDealCycleByProduct(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-customer/get-customer-deal-cycle-by-product"
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
