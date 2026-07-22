import time
import pytest
from config import ADMIN_URL


class TestMemberLevelCreate:
    """创建会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/level/create"
        level_num = int(time.time()) % 100000 + 100  # 避开 fixture 的级别
        body = {"name": f"autotest_CL{level_num}", "level": level_num, "experience": level_num * 100, "discountPercent": 100, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        print(f"RESP: {resp.text[:300]}")
        assert resp.status_code == 200
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
