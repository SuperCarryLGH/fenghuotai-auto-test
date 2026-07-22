import pytest
from config import ADMIN_URL


class TestCrmStatisticsPortraitGetCustomerAreaSummary:
    """获取客户地区统计数据"""

    @pytest.mark.smoke
    def test_CrmStatisticsPortraitGetCustomerAreaSummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-portrait/get-customer-area-summary"
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
