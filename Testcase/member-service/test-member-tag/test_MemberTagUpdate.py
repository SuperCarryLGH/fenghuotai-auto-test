import pytest
from config import ADMIN_URL


class TestMemberTagUpdate:
    """更新会员标签"""

    @pytest.mark.smoke
    def test_MemberTagUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/tag/update"
        body = {"id": autotest_tag_id}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
