import pytest
from config import ADMIN_URL


class TestSystemRoleExportExcel:
    """导出角色 Excel"""

    @pytest.mark.smoke
    def test_SystemRoleExportExcel(self, api_session, auth_headers, autotest_role_id):
        url = f"{ADMIN_URL}/admin-api/system/role/export-excel"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
