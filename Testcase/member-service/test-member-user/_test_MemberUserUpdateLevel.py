import pytest
from config import ADMIN_URL


class TestMemberUserUpdateLevel:
    """---"""

    @pytest.mark.smoke
    def test_MemberUserUpdateLevel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/user/update-level"
        body = {"id": 2071418043802406914, "levelId": 1}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
