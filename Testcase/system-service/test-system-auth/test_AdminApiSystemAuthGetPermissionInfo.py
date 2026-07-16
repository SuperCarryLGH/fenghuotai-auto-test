import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiSystemAuthGetPermissionInfo:
    """获取登录用户的权限信息"""

    @pytest.mark.smoke
    def test_AdminApiSystemAuthGetPermissionInfo(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/get-permission-info"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
