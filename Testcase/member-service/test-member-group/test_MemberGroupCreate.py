import pytest
from config import ADMIN_URL


class TestMemberGroupCreate:
    """创建用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/group/create"
        body = {"name": f"分组_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
