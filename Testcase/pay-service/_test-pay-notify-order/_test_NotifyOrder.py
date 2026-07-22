import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class TestNotifyOrder:
    """支付订单回调通知（{channelId} 替换为具体支付渠道ID）"""

    @pytest.mark.smoke
    def test_NotifyOrder(self, api_session, auth_headers):
        channel_id = common["common"]["id"]["valid"]
        url = f"{ADMIN_URL}/admin-api/pay/notify/order/{channel_id}"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
