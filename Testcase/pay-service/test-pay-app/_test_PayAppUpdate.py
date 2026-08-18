import pytest
from config import ADMIN_URL


class TestPayAppUpdate:
    """更新支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/app/update"
        body = {
              "appKey": "autotest",
              "name": "autotest",
              "status": 1,
              "remark": "autotest update",
              "orderNotifyUrl": "http://autotest/pay-callback",
              "refundNotifyUrl": "http://autotest/refund-callback",
              "transferNotifyUrl": "http://autotest/transfer-callback",
              "id": 2077228704176402434
            }
        ok(api_session.put(url, json=body, headers=auth_headers))
