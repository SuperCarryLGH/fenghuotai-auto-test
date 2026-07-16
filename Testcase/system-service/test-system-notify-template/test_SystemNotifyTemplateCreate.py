import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateCreate:
    """创建站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/create"
        body = {"name": f"通知模板_194199", "code": f"NTF_194199", "content": "测试内容", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
