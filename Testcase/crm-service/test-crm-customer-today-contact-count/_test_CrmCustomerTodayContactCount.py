import pytest
from config import ADMIN_URL


class TestCrmCustomerTodayContactCount:
    """获得今日需联系客户数量"""

    @pytest.mark.smoke
    def test_CrmCustomerTodayContactCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/today-contact-count"
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
