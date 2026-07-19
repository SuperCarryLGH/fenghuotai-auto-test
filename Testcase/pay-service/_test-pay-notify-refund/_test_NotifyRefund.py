import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class TestNotifyRefund:
    """退款回调通知"""

    @pytest.mark.smoke
    def test_NotifyRefund(self, api_session, auth_headers):
        channel_id = common["common"]["id"]["valid"]
        url = f"{ADMIN_URL}/admin-api/pay/notify/refund/{channel_id}"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
