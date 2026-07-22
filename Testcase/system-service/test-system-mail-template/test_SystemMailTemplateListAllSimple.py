import pytest
from config import ADMIN_URL


class TestSystemMailTemplateListAllSimple:
    """获得邮件模版精简列表"""

    @pytest.mark.smoke
    def test_SystemMailTemplateListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
