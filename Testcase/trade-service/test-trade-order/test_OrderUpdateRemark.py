import pytest
from config import ADMIN_URL


class TestOrderUpdateRemark:
    """订单备注"""

    @pytest.mark.smoke
    def test_OrderUpdateRemark(self, api_session, auth_headers, order_id, ok):
        url = f"{ADMIN_URL}/admin-api/trade/order/update-remark"
        body = {
            "id": order_id,
            "remark": "测试备注",
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
