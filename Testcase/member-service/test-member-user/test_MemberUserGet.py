import pytest
from config import ADMIN_URL


class TestMemberUserGet:
    """获得会员用户"""

    @pytest.mark.smoke
    def test_MemberUserGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/user/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
