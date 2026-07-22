import pytest
from config import ADMIN_URL


class TestCrmStatisticsCustomerGetContractSummary:
    """获取客户的首次合同、回款信息列表"""

    @pytest.mark.smoke
    def test_CrmStatisticsCustomerGetContractSummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/statistics-customer/get-contract-summary"
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
