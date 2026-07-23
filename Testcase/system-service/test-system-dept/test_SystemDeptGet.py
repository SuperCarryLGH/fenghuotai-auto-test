import pytest
from config import ADMIN_URL


class TestSystemDeptGet:
    """获得部门信息"""

    @pytest.mark.smoke
    def test_SystemDeptGet(self, api_session, auth_headers, autotest_dept_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/dept/get"
        params = {"id": autotest_dept_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
