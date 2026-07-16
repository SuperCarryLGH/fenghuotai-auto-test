import pytest
from config import ADMIN_URL


class TestPayAppCreate:
    """创建支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/app/create"
        body = {
              "appKey": "autotest",
              "name": "autotest",
              "status": 1,
              "remark": "autotest",
              "orderNotifyUrl": "http://autotest/pay-callback",
              "refundNotifyUrl": "http://autotest/refund-callback",
              "transferNotifyUrl": "http://autotest/transfer-callback"
            }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
