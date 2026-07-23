import pytest
from config import ADMIN_URL


class TestSystemOperateAreaCreate:
    """创建系统-运营区域管理"""

    @pytest.mark.smoke
    def test_SystemOperateAreaCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/operate-area/create"
        body = {"name": f"autotest_194199", "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
