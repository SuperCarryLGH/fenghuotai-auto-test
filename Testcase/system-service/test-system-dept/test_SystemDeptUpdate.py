import pytest
from config import ADMIN_URL


class TestSystemDeptUpdate:
    """更新部门"""

    @pytest.mark.smoke
    def test_SystemDeptUpdate(self, api_session, auth_headers, autotest_dept_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/dept/update"
        body = {"id": autotest_dept_id, "name": "autotest_update", "sort": 0, "status": 0}
        r = ok(api_session.put(url, json=body, headers=auth_headers))
        print(r)
