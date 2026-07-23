import pytest
from config import ADMIN_URL


class TestPayOrderGet:
    """获得支付订单"""

    @pytest.mark.smoke
    def test_PayOrderGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/order/get"
        params = {"id": 15617637160}
        ok(api_session.get(url, params=params, headers=auth_headers))
