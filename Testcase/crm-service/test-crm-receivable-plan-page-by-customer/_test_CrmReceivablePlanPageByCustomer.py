import pytest
from config import ADMIN_URL


class TestCrmReceivablePlanPageByCustomer:
    """获得回款计划分页，基于指定客户"""

    @pytest.mark.smoke
    def test_CrmReceivablePlanPageByCustomer(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/receivable-plan/page-by-customer"
        params = {
            # TODO: 补充查询参数
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
