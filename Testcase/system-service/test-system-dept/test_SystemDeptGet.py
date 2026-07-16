import pytest
from config import ADMIN_URL


class TestSystemDeptGet:
    """获得部门信息"""

    @pytest.mark.smoke
    def test_SystemDeptGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dept/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
