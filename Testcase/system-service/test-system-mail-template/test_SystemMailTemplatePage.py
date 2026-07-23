import pytest
from config import ADMIN_URL


class TestSystemMailTemplatePage:
    """获得邮件模版分页"""

    @pytest.mark.smoke
    def test_SystemMailTemplatePage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
