import pytest
from config import ADMIN_URL


class TestMemberUserGet:
    """获得会员用户"""

    @pytest.mark.smoke
    def test_MemberUserGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/user/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        ok(api_session.get(url, params=params, headers=auth_headers))
