import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplateGet:
    """获得站内信模版"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplateGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/get"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
