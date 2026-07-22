import pytest
from config import ADMIN_URL


class TestMemberTagListAllSimple:
    """获取会员标签精简信息列表"""

    @pytest.mark.smoke
    def test_MemberTagListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/tag/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
