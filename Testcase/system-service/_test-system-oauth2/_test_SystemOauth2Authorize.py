import pytest
from config import ADMIN_URL


class TestSystemOauth2Authorize:
    """获得授权信息"""

    @pytest.mark.smoke
    def test_SystemOauth2Authorize(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2/authorize"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
