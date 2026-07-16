import pytest
from config import ADMIN_URL


class TestMemberTagCreate:
    """创建会员标签"""

    @pytest.mark.smoke
    def test_MemberTagCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/tag/create"
        body = {"name": f"标签_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
