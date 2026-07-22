import time
import pytest
from config import ADMIN_URL
from Common.loader import load_yaml

users = load_yaml("batch_users.yaml")["batch_users"]


class TestBatchCreateUser:
    """新增用户"""

    @pytest.mark.smoke
    @pytest.mark.parametrize("user", users, ids=[u["desc"] for u in users])
    def test_create_user(self, api_session, auth_headers, user):
        url = f"{ADMIN_URL}/admin-api/system/user/create"
        suffix = str(int(time.time()))[-8:]
        payload = {
            "username": f"{user['username']}{suffix}",
            "password": user["password"],
            "nickname": f"{user['nickname']}{suffix}",
            "mobile": user["mobile"],
            "sex": user["sex"],
            "status": user["status"],
        }

        resp = api_session.post(url, json=payload, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
