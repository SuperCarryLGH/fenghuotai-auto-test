import pytest
from config import ADMIN_URL


class TestMemberUserUpdate:
    """更新会员用户"""

    @pytest.mark.smoke
    def test_MemberUserUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/user/update"
        body = {"id": 1, "nickname": f"更新用户_194200", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
