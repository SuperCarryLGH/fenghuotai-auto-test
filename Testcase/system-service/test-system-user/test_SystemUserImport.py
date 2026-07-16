import pytest
from config import ADMIN_URL


class TestSystemUserImport:
    """导入用户"""

    @pytest.mark.smoke
    def test_SystemUserImport(self, api_session, auth_headers, system_user_id):
        url = f"{ADMIN_URL}/admin-api/system/user/import"
        # 导入接口，需构造 multipart/form-data + 文件
        body = {
            # TODO: 补充创建参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
