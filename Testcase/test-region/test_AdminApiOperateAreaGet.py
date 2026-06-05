import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiOperateAreaGet:
    """admin获取运营区域详情"""

    @pytest.mark.smoke
    def test_AdminApiOperateAreaGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
