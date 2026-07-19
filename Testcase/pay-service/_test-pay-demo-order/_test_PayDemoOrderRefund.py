import pytest
from config import ADMIN_URL


class TestPayDemoOrderRefund:
    """发起示例订单的退款"""

    @pytest.mark.smoke
    def test_PayDemoOrderRefund(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-order/refund"
        body = {"id": "_pay_demo_order_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
