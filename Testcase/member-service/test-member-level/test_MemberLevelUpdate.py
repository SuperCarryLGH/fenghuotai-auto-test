import time
import pytest
from config import ADMIN_URL


class TestMemberLevelUpdate:
    """更新会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelUpdate(self, api_session, auth_headers, ok, autotest_level_id):
        url = f"{ADMIN_URL}/admin-api/member/level/update"
        level_num = getattr(autotest_level_id, 'level_num', str(int(time.time()))[-6:])
        body = {"id": autotest_level_id, "name": f"autotest_UPD_{str(int(time.time()))[-6:]}", 
                "level": level_num, "experience": int(level_num) * 100, 
                "discountPercent": 100, "remark": "autotest", "status": 1}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
