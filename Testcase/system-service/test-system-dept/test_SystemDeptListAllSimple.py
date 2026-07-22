import pytest
from config import ADMIN_URL


class TestSystemDeptListAllSimple:
    """获取部门精简信息列表"""

    @pytest.mark.smoke
    def test_SystemDeptListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/dept/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
