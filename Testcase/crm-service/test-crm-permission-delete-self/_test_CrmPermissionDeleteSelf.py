import pytest
from config import ADMIN_URL


class TestCrmPermissionDeleteSelf:
    """删除自己的数据权限"""

    @pytest.mark.smoke
    def test_CrmPermissionDeleteSelf(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/permission/delete-self"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
