import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateDeleteList:
    """批量删除站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateDeleteList(self, api_session, auth_headers, autotest_notify_template_id, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/delete-list"
        params = {"ids": str(autotest_notify_template_id)}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
