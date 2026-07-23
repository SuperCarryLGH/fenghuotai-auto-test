import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateUpdate:
    """更新站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateUpdate(self, api_session, auth_headers, autotest_notify_template_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/update"
        import time
        body = {"id": autotest_notify_template_id, "name": f"notify_{int(time.time())}", "code": f"NTF_{int(time.time())}", "type": 1, "nickname": "autotest", "content": "autotest_updated", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
