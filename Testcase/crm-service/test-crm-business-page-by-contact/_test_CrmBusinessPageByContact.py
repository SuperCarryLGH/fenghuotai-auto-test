import pytest
from config import ADMIN_URL


class TestCrmBusinessPageByContact:
    """获得联系人的商机分页"""

    @pytest.mark.smoke
    def test_CrmBusinessPageByContact(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/business/page-by-contact"
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
