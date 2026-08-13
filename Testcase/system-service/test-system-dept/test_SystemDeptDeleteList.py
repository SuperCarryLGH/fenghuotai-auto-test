import pytest
from config import ADMIN_URL


class TestSystemDeptDeleteList:
    """批量删除部门"""

    @pytest.mark.smoke
    def test_SystemDeptDeleteList(self, api_session, auth_headers, autotest_dept_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/dept/delete-list"
        body = {"ids": str(autotest_dept_id)}
        r = ok(api_session.delete(url, params=body, headers=auth_headers))
        print(r)
