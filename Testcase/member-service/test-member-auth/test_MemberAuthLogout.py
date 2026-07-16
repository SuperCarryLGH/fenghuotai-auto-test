import pytest
from config import APP_URL


class TestMemberAuthLogout:
    """登出系统"""

    @pytest.mark.smoke
    def test_MemberAuthLogout(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/logout"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
