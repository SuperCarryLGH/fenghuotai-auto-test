import pytest
from config import ADMIN_URL


class TestMemberLevelDelete:
    """删除会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelDelete(self, api_session, auth_headers, autotest_level_id, ok):
        url = f"{ADMIN_URL}/admin-api/member/level/delete"
        params = {"id": autotest_level_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
