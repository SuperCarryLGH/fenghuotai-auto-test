import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateCreate:
    """创建站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/create"
        import time
        body = {"name": f"通知模板_{int(time.time())}", "code": f"NTF_{int(time.time())}", "content": "测试内容", "type": 1, "nickname": "autotest", "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
