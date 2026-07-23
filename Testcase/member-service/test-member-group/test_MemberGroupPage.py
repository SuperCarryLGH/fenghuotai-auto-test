import pytest
from config import ADMIN_URL


class TestMemberGroupPage:
    """获得用户分组分页"""

    @pytest.mark.smoke
    def test_MemberGroupPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/group/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
