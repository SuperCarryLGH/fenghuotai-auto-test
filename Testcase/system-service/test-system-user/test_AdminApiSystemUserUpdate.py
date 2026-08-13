import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemUserUpdate:
    """修改用户"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserUpdate(self, api_session, auth_headers, autotest_user_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update"
        suffix = str(int(time.time()))
        body = {
            "id": autotest_user_id,
            "username": f"upd{suffix[-8:]}",
            "nickname": f"更新用户_{suffix}",
            "mobile": f"186{suffix[-8:]}",
            "status": 0,
        }
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
