import pytest
from config import ADMIN_URL


class TestSystemDeptDeleteList:
    """批量删除部门"""

    @pytest.mark.smoke
    def test_SystemDeptDeleteList(self, api_session, auth_headers, autotest_dept_id):
        url = f"{ADMIN_URL}/admin-api/system/dept/delete-list"
        # ⚠️ 敏感操作 — 参数已补全，确认后再执行
        body = {"ids": str(autotest_dept_id)}  # 来自 conftest fixture
        # resp = api_session.delete(url, json=body, headers=auth_headers)
        # assert resp.status_code == 200
        # r = resp.json()
        # assert r["code"] == 0
        # print(r)
