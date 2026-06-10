import pytest
from config import ADMIN_URL


class TestCreateUser:
    """单次创建用户"""

    @pytest.mark.smoke
    def test_create_user(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/create"
        payload = {
            "username": "00000001",
            "password": "00000001",
            "nickname": "西音",
            "mobile": "19500000001",
            "sex": 1,
            "status": 0,
        }

        resp = api_session.post(url, json=payload, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
