import pytest
from config import ADMIN_URL


class TestCrmCustomerFollowCount:
    """获得分配给我、待跟进的线索数量的客户数量"""

    @pytest.mark.smoke
    def test_CrmCustomerFollowCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/follow-count"
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
