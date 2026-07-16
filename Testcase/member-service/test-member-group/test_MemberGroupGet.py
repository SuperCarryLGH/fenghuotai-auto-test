import pytest
from config import ADMIN_URL


class TestMemberGroupGet:
    """获得用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/group/get"
        params = {"id": "member_group_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
