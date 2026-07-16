import pytest
from config import ADMIN_URL


class TestCrmStatisticsCustomerGetFollowUpSummaryByType:
    """获取客户跟进次数分析(按类型)"""

    @pytest.mark.smoke
    def test_CrmStatisticsCustomerGetFollowUpSummaryByType(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-customer/get-follow-up-summary-by-type"
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
