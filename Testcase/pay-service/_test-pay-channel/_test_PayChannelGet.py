import pytest
from config import ADMIN_URL


class TestPayChannelGet:
    """获得支付渠道"""

    @pytest.mark.smoke
    def test_PayChannelGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/channel/get"
        params = {
            "id" : 2077228704176402434
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
