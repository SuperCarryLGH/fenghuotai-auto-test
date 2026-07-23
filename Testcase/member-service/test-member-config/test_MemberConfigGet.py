import pytest
from config import ADMIN_URL


class TestMemberConfigGet:
    """获得会员配置"""

    @pytest.mark.smoke
    def test_MemberConfigGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/config/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        ok(api_session.get(url, params=params, headers=auth_headers))
