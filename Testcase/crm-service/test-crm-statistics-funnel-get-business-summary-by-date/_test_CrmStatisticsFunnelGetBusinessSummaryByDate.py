import pytest
from config import ADMIN_URL


class TestCrmStatisticsFunnelGetBusinessSummaryByDate:
    """获取新增商机分析(按日期)"""

    @pytest.mark.smoke
    def test_CrmStatisticsFunnelGetBusinessSummaryByDate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-funnel/get-business-summary-by-date"
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
