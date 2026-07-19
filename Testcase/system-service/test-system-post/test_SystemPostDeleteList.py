import pytest
from config import ADMIN_URL


class TestSystemPostDeleteList:
    """批量删除岗位"""

    @pytest.mark.smoke
    def test_SystemPostDeleteList(self, api_session, auth_headers, autotest_post_id):
        url = f"{ADMIN_URL}/admin-api/system/post/delete-list"
        params = {"ids": str(autotest_post_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
