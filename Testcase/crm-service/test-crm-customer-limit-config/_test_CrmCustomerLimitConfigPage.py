import pytest
from config import ADMIN_URL


class TestCrmCustomerLimitConfigPage:
    """获得客户限制配置分页"""

    @pytest.mark.smoke
    def test_CrmCustomerLimitConfigPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer-limit-config/page"
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
