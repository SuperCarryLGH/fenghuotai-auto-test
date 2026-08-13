import pytest
from config import ADMIN_URL


class TestMemberGroupListAllSimple:
    """获取会员分组精简信息列表"""

    @pytest.mark.smoke
    def test_MemberGroupListAllSimple(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/group/list-all-simple"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
