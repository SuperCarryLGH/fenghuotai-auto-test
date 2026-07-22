import pytest
from config import ADMIN_URL


class TestCrmCustomerPoolConfigSave:
    """更新客户公海规则设置"""

    @pytest.mark.smoke
    def test_CrmCustomerPoolConfigSave(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer-pool-config/save"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
