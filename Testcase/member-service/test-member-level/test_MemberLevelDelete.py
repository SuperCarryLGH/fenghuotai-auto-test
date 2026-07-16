import pytest
from config import ADMIN_URL


class TestMemberLevelDelete:
    """删除会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/level/delete"
        params = {"id": "member_level_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
