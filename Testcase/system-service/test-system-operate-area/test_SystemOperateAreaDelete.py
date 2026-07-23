import pytest
from config import ADMIN_URL


class TestSystemOperateAreaDelete:
    """删除系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaDelete(self, api_session, auth_headers, autotest_operate_area_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/delete"
        params = {"id": autotest_operate_area_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
