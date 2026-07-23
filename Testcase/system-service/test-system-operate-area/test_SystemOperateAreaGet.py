import pytest
from config import ADMIN_URL


class TestSystemOperateAreaGet:
    """获得系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaGet(self, api_session, auth_headers, autotest_operate_area_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/get"
        params = {"id": autotest_operate_area_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
