import pytest
from config import ADMIN_URL


class TestCrmStatisticsFunnelGetBusinessSummaryByEndStatus:
    """获取商机结束状态统计"""

    @pytest.mark.smoke
    def test_CrmStatisticsFunnelGetBusinessSummaryByEndStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-funnel/get-business-summary-by-end-status"
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
