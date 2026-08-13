import pytest
from config import ADMIN_URL


class TestSystemMailAccountSimpleList:
    """获得邮箱账号精简列表"""

    @pytest.mark.smoke
    def test_SystemMailAccountSimpleList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-account/simple-list"
        params = {}
        r = ok(api_session.get(url, params=params, headers=auth_headers))
        print(r)
