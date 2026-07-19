import pytest
from config import ADMIN_URL


class TestSystemSmsChannelListAllSimple:
    """获得短信渠道精简列表"""

    @pytest.mark.smoke
    def test_SystemSmsChannelListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/sms-channel/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
