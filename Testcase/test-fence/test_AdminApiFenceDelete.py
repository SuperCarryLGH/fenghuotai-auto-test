import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiFenceDelete:
    """admin删除电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/fence/delete"
        params = {"id": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
