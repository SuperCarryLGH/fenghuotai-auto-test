import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemDictDataGet:
    """-查询字典数据详细"""

    @pytest.mark.smoke
    def test_AdminApiSystemDictDataGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
