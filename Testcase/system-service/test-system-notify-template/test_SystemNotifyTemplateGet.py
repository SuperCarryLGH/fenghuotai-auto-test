import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateGet:
    """获得站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateGet(self, api_session, auth_headers, autotest_notify_template_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/get"
        params = {"id": autotest_notify_template_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
