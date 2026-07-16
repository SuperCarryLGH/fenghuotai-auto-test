import pytest
from config import ADMIN_URL


class TestSystemOperateAreaGet:
    """获得系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
