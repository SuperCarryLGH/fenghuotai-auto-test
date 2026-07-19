import pytest
from config import ADMIN_URL


class TestSystemSmsChannelDelete:
    """删除短信渠道"""

    @pytest.mark.smoke
    def test_SystemSmsChannelDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-channel/delete"
        params = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
