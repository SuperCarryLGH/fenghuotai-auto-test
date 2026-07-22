import pytest
from config import ADMIN_URL


class TestCrmContactPageByBusiness:
    """获得联系人分页，基于指定商机"""

    @pytest.mark.smoke
    def test_CrmContactPageByBusiness(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contact/page-by-business"
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
