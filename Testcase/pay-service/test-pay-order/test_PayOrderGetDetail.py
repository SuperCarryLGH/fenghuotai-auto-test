import pytest
from config import ADMIN_URL


class TestPayOrderGetDetail:
    """获得支付订单详情"""

    @pytest.mark.smoke
    def test_PayOrderGetDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/order/get-detail"
        params = {"id": 15617637160}
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
