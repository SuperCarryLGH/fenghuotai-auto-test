import pytest
from config import ADMIN_URL


class TestSystemDictTypeGet:
    """-查询字典类型详细"""

    @pytest.mark.smoke
    def test_SystemDictTypeGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
