import pytest
from config import ADMIN_URL


class TestSystemMailTemplateDeleteList:
    """批量删除邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateDeleteList(self, api_session, auth_headers, autotest_mail_template_id):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/delete-list"
        params = {"ids": str(autotest_mail_template_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
