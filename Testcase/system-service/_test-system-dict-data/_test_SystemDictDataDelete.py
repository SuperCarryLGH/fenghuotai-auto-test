import pytest
from config import ADMIN_URL


class TestSystemDictDataDelete:
    """删除字典数据"""

    @pytest.mark.smoke
    def test_SystemDictDataDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dict-data/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
