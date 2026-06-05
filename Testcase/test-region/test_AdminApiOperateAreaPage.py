import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaPage:
    """admin运营区域分页"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
