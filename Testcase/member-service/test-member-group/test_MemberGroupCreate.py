import pytest
from config import ADMIN_URL


class TestMemberGroupCreate:
    """创建用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/group/create"
        body = {"name": f"分组_194200", "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
