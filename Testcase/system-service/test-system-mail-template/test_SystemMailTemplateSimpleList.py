import pytest
from config import ADMIN_URL


class TestSystemMailTemplateSimpleList:
    """获得邮件模版精简列表"""

    @pytest.mark.smoke
    def test_SystemMailTemplateSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
