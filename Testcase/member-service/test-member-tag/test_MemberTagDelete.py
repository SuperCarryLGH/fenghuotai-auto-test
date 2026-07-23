import pytest
from config import ADMIN_URL


class TestMemberTagDelete:
    """删除会员标签"""

    @pytest.mark.smoke
    def test_MemberTagDelete(self, api_session, auth_headers, autotest_tag_id, ok):
        url = f"{ADMIN_URL}/admin-api/member/tag/delete"
        params = {"id": autotest_tag_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
