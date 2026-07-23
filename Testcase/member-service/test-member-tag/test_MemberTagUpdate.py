import time
import pytest
from config import ADMIN_URL


class TestMemberTagUpdate:
    """更新会员标签"""

    @pytest.mark.smoke
    def test_MemberTagUpdate(self, api_session, auth_headers, autotest_tag_id, ok):
        url = f"{ADMIN_URL}/admin-api/member/tag/update"
        body = {"id": autotest_tag_id, "name": f"autotest_upd_{str(int(time.time()))[-6:]}", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
