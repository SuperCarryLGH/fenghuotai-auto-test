import pytest
from config import ADMIN_URL


class TestPayDemoOrderUpdateRefunded:
    """更新示例订单为已退款"""

    @pytest.mark.smoke
    def test_PayDemoOrderUpdateRefunded(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-order/update-refunded"
        body = {"id": "_pay_demo_order_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
