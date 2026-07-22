import pytest
from config import ADMIN_URL


class TestSystemOperateAreaUpdate:
    """更新系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaUpdate(self, api_session, auth_headers, autotest_operate_area_id):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/update"
        body = {"id": autotest_operate_area_id}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
