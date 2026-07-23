import pytest
from config import ADMIN_URL


class TestSystemOperateAreaUpdate:
    """更新系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaUpdate(self, api_session, auth_headers, autotest_operate_area_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/update"
        body = {"id": autotest_operate_area_id}  # 来自 conftest fixture
        ok(api_session.put(url, json=body, headers=auth_headers))
