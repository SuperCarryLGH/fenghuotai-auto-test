import pytest
import time
from Common.login import Login
from config import APP_URL


class TestMemberSocialUserUnbind:
    """取消社交绑定"""

    @pytest.mark.smoke
    def test_MemberSocialUserUnbind(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/member/social-user/unbind"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        body = {"id": 1}  # TODO: 替换为实际 ID
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
