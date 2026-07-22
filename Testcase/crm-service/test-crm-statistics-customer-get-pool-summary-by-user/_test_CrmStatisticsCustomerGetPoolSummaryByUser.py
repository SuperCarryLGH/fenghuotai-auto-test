import pytest
from config import ADMIN_URL


class TestCrmStatisticsCustomerGetPoolSummaryByUser:
    """获取公海客户分析(按用户)"""

    @pytest.mark.smoke
    def test_CrmStatisticsCustomerGetPoolSummaryByUser(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-customer/get-pool-summary-by-user"
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
