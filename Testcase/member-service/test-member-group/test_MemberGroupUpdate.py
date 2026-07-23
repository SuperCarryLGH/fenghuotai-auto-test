import time
import pytest
from config import ADMIN_URL


class TestMemberGroupUpdate:
    """更新用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupUpdate(self, api_session, auth_headers, autotest_group_id, ok):
        url = f"{ADMIN_URL}/admin-api/member/group/update"
        body = {"id": autotest_group_id, "name": f"autotest_upd_{str(int(time.time()))[-6:]}", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
