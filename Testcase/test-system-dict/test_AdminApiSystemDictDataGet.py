import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemDictDataGet:
    """admin获取字典数据"""

    @pytest.mark.smoke
    def test_AdminApiSystemDictDataGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
