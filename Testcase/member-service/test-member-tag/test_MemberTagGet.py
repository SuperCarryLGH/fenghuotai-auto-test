import pytest
from config import ADMIN_URL


class TestMemberTagGet:
    """获得会员标签"""

    @pytest.mark.smoke
    def test_MemberTagGet(self, api_session, auth_headers, autotest_tag_id):
        url = f"{ADMIN_URL}/admin-api/member/tag/get"
        params = {"id": autotest_tag_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
