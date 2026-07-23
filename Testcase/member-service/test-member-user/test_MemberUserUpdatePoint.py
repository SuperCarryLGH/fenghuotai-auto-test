import pytest
from config import ADMIN_URL


class TestMemberUserUpdatePoint:
    """---"""

    @pytest.mark.smoke
    def test_MemberUserUpdatePoint(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/user/update-point"
        body = {"id": 2071418043802406914, "point": 100}
        ok(api_session.put(url, json=body, headers=auth_headers))
