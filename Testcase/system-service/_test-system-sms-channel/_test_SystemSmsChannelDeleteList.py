import pytest
from config import ADMIN_URL


class TestSystemSmsChannelDeleteList:
    """批量删除短信渠道"""

    @pytest.mark.smoke
    def test_SystemSmsChannelDeleteList(self, api_session, auth_headers, autotest_sms_channel_id):
        url = f"{ADMIN_URL}/admin-api/system/sms-channel/delete-list"
        params = {"ids": str(autotest_sms_channel_id)}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
