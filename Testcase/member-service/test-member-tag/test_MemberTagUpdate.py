import time
import pytest
from config import ADMIN_URL


class TestMemberTagUpdate:
    """更新会员标签"""

    @pytest.mark.smoke
    def test_MemberTagUpdate(self, api_session, auth_headers, autotest_tag_id):
        url = f"{ADMIN_URL}/admin-api/member/tag/update"
        body = {"id": autotest_tag_id, "name": f"autotest_upd_{str(int(time.time()))[-6:]}", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
