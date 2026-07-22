import pytest
from config import ADMIN_URL


class TestSystemOperateAreaDeleteList:
    """批量删除系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaDeleteList(self, api_session, auth_headers, autotest_operate_area_id):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/delete-list"
        params = {"ids": str(autotest_operate_area_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
