import pytest
from config import ADMIN_URL


class TestMemberUserPage:
    """获得会员用户分页"""

    @pytest.mark.smoke
    def test_MemberUserPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/user/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
