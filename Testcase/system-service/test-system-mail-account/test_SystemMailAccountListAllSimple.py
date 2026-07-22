import pytest
from config import ADMIN_URL


class TestSystemMailAccountListAllSimple:
    """获得邮箱账号精简列表"""

    @pytest.mark.smoke
    def test_SystemMailAccountListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
