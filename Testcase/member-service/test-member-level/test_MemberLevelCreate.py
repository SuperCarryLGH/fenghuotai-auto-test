import pytest
from config import ADMIN_URL


class TestMemberLevelCreate:
    """创建会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/level/create"
        body = {"name": f"等级_194200", "level": 0, "experience": 100, "discountPercent": 100, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
