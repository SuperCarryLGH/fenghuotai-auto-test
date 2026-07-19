import pytest
from config import ADMIN_URL


class TestSystemSmsTemplateUpdate:
    """更新短信模板"""

    @pytest.mark.smoke
    def test_SystemSmsTemplateUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-template/update"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
