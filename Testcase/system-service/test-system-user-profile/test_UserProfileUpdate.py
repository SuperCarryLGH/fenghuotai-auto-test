import pytest
from config import ADMIN_URL


class TestUserProfileUpdate:
    """修改用户个人信息"""

    @pytest.mark.smoke
    def test_UserProfileUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/profile/update"
        body = {"id": 1, "nickname": f"更新用户_194199", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
