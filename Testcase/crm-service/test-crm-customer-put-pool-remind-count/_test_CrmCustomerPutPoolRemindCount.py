import pytest
from config import ADMIN_URL


class TestCrmCustomerPutPoolRemindCount:
    """获得待进入公海客户数量"""

    @pytest.mark.smoke
    def test_CrmCustomerPutPoolRemindCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/put-pool-remind-count"
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
