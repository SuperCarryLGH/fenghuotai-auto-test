import pytest
from config import ADMIN_URL


class TestSystemUserGetImportTemplate:
    """获得导入用户模板"""

    @pytest.mark.smoke
    def test_SystemUserGetImportTemplate(self, api_session, auth_headers, autotest_user_id):
        url = f"{ADMIN_URL}/admin-api/system/user/get-import-template"
        params = {"id": autotest_user_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
