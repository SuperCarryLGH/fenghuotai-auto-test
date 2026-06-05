import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemPostPage:
    """admin岗位分页"""

    @pytest.mark.smoke
    def test_AdminApiSystemPostPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/post/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
