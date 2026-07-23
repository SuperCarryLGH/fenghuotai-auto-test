import time
import pytest
from config import ADMIN_URL


class TestPayAppCreate:
    """创建支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/app/create"
        suffix = str(int(time.time()))
        body = {
              "appKey": f"autotest_{suffix}",
              "name": f"autotest_{suffix}",
              "status": 1,
              "remark": "autotest",
              "orderNotifyUrl": "http://autotest/pay-callback",
              "refundNotifyUrl": "http://autotest/refund-callback",
              "transferNotifyUrl": "http://autotest/transfer-callback"
            }
        ok(api_session.post(url, json=body, headers=auth_headers))
