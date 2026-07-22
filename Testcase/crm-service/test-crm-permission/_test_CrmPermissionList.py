import pytest
from config import ADMIN_URL


class TestCrmPermissionList:
    """获得数据权限列表"""

    @pytest.mark.smoke
    def test_CrmPermissionList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/permission/list"
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
