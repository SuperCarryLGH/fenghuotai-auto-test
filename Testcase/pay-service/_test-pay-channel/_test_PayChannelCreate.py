import pytest
from config import ADMIN_URL


class TestPayChannelCreate:
    """创建支付渠道"""

    @pytest.mark.smoke
    def test_PayChannelCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/channel/create"
        body = {
              "status": 0,
              "remark": "autotest",
              "feeRate": 10,
              "appId": 2077228704176402434,
              "code": "alipay_pc",
              "config": "",
            }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
