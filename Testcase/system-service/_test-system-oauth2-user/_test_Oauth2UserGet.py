import pytest
from config import ADMIN_URL


class TestOauth2UserGet:
    """获得用户基本信息"""

    @pytest.mark.smoke
    def test_Oauth2UserGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2/user/get"
        params = {}  # TODO: 替换为实际存在的 ID
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
