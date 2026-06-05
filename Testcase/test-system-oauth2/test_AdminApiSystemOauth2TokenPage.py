import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemOauth2TokenPage:
    """admin令牌分页"""

    @pytest.mark.smoke
    def test_AdminApiSystemOauth2TokenPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/oauth2-token/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
