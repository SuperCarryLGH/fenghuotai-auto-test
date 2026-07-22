import pytest
from config import ADMIN_URL


class TestBpmUserGroupPage:
    """获得用户组分页"""

    @pytest.mark.smoke
    def test_BpmUserGroupPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/user-group/page"
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
