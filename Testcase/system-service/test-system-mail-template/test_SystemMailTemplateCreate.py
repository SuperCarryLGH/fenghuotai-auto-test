import pytest
from config import ADMIN_URL


class TestSystemMailTemplateCreate:
    """创建邮件模版"""

    @pytest.mark.smoke
    def test_SystemMailTemplateCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/mail-template/create"
        body = {"name": f"邮件模板_194199", "code": f"MAIL_194199", "title": "测试", "content": "测试内容", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
