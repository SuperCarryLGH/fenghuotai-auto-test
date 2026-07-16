import pytest
from config import ADMIN_URL


class TestPayChannelDelete:
    """删除支付渠道"""

    @pytest.mark.smoke
    def test_PayChannelDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/channel/delete"
        params = {
            "id": 1,
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
