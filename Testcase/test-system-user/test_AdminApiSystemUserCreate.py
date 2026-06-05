import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_user

common = load_common()
user_data = load_system_user()


class Test_AdminApiSystemUserCreate:
    """admin新增用户"""

    @pytest.mark.smoke
    def test_AdminApiSystemUserCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/create"
        suffix = str(int(time.time()))
        body = {
            "username": f"{user_data['user']['create']['username']}_{suffix}",
            "password": user_data['user']['create']['password'],
            "nickname": f"测试用户_{suffix}",
            "mobile": f"186{suffix[-8:]}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
