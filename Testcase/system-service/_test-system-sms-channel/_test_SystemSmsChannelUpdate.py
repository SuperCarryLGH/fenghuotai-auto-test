import pytest
from config import ADMIN_URL


class TestSystemSmsChannelUpdate:
    """更新短信渠道"""

    @pytest.mark.smoke
    def test_SystemSmsChannelUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-channel/update"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
