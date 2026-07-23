import pytest
from config import ADMIN_URL


class TestMemberGroupDelete:
    """删除用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupDelete(self, api_session, auth_headers, autotest_group_id, ok):
        url = f"{ADMIN_URL}/admin-api/member/group/delete"
        params = {"id": autotest_group_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
