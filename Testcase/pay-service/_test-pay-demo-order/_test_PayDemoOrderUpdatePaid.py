import pytest
from config import ADMIN_URL


class TestPayDemoOrderUpdatePaid:
    """更新示例订单为已支付"""

    @pytest.mark.smoke
    def test_PayDemoOrderUpdatePaid(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-order/update-paid"
        body = {"id": "_pay_demo_order_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
