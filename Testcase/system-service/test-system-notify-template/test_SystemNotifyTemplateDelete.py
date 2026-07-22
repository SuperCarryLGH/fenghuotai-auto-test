import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateDelete:
    """删除站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateDelete(self, api_session, auth_headers, autotest_notify_template_id):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/delete"
        params = {"id": autotest_notify_template_id}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
