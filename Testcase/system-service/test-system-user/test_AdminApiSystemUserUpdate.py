import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemUserUpdate:
    """修改用户"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/user/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "username": f"update_user_{suffix}",
            "nickname": f"更新用户_{suffix}",
            "mobile": f"186{suffix[-8:]}",
            "status": common['common']['status']['enabled'],
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
