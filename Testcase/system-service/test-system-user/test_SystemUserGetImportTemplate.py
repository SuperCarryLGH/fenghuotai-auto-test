import pytest
from config import ADMIN_URL


class TestSystemUserGetImportTemplate:
    """获得导入用户模板"""

    @pytest.mark.smoke
    def test_SystemUserGetImportTemplate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/user/get-import-template"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
        print(f"模板下载成功, 文件大小={len(resp.content)}bytes")
