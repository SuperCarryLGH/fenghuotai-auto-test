import time
import pytest
from config import ADMIN_URL


class TestMemberTagCreate:
    """创建会员标签"""

    @pytest.mark.smoke
    def test_MemberTagCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/tag/create"
        body = {"name": f"autotest_tag_{str(int(time.time()))[-6:]}", "status": 0}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
