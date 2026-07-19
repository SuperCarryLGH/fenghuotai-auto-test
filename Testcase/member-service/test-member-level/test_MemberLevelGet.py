import pytest
from config import ADMIN_URL


class TestMemberLevelGet:
    """获得会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/level/get"
        params = {"id": autotest_level_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
