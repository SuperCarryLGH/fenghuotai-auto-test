import pytest
from config import ADMIN_URL


class TestCrmStatisticsPortraitGetCustomerSourceSummary:
    """获取客户来源统计数据"""

    @pytest.mark.smoke
    def test_CrmStatisticsPortraitGetCustomerSourceSummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-portrait/get-customer-source-summary"
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
