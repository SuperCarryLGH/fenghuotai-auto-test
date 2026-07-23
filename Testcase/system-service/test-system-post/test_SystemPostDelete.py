import pytest
from config import ADMIN_URL


class TestSystemPostDelete:
    """删除岗位"""

    @pytest.mark.smoke
    def test_SystemPostDelete(self, api_session, auth_headers, autotest_post_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/delete"
        params = {"id": autotest_post_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
