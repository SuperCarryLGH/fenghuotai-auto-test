import pytest
from config import ADMIN_URL


class TestSystemOperateAreaDelete:
    """删除系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
