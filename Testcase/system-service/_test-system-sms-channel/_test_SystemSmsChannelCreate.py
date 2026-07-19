import pytest
from config import ADMIN_URL


class TestSystemSmsChannelCreate:
    """创建短信渠道"""

    @pytest.mark.smoke
    def test_SystemSmsChannelCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-channel/create"
        body = {"signature": f"测试_194199", "code": f"AUTO_194199", "apiKey": "test", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
