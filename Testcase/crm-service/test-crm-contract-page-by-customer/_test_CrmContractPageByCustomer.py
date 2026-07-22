import pytest
from config import ADMIN_URL


class TestCrmContractPageByCustomer:
    """获得合同分页，基于指定客户"""

    @pytest.mark.smoke
    def test_CrmContractPageByCustomer(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contract/page-by-customer"
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
