import pytest
from config import ADMIN_URL


class TestPayChannelUpdate:
    """更新支付渠道"""

    @pytest.mark.smoke
    def test_PayChannelUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/channel/update"
        body = {"id": "_pay_channel_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
