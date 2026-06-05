import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemPostGet:
    """admin获取岗位"""

    @pytest.mark.smoke
    def test_AdminApiSystemPostGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/post/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
