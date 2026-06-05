import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemAuthRefreshToken:
    """admin刷新令牌"""

    @pytest.mark.smoke
    def test_AdminApiSystemAuthRefreshToken(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/refresh-token"
        params = {"refreshToken": "test_refresh_token"}
        resp = api_session.post(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        print(r)
