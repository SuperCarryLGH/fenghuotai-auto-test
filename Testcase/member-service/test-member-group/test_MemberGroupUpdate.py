import time
import pytest
from config import ADMIN_URL


class TestMemberGroupUpdate:
    """更新用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupUpdate(self, api_session, auth_headers, autotest_group_id):
        url = f"{ADMIN_URL}/admin-api/member/group/update"
        body = {"id": autotest_group_id, "name": f"autotest_upd_{str(int(time.time()))[-6:]}", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
