import pytest
from config import ADMIN_URL


class TestMemberLevelListAllSimple:
    """获取会员等级精简信息列表"""

    @pytest.mark.smoke
    def test_MemberLevelListAllSimple(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/level/list-all-simple"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
