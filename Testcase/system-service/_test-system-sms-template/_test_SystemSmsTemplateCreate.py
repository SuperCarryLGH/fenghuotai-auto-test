import pytest
from config import ADMIN_URL


class TestSystemSmsTemplateCreate:
    """创建短信模板"""

    @pytest.mark.smoke
    def test_SystemSmsTemplateCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-template/create"
        body = {"name": f"模板_194199", "code": f"TMPL_194199", "content": "测试内容", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
