import time
import pytest
from config import ADMIN_URL


class TestMemberTagCreate:
    """创建会员标签"""

    @pytest.mark.smoke
    def test_MemberTagCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/tag/create"
        body = {"name": f"autotest_tag_{str(int(time.time()))[-6:]}", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        r = resp.json()
        print(f"CREATE RESP: code={r.get('code')}, msg={r.get('msg','')}")
        assert resp.status_code == 200
        assert r["code"] == 0
        print(r)
