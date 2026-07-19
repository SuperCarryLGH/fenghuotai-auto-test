import pytest
from config import ADMIN_URL


class TestPayOrderGet:
    """获得支付订单"""

    @pytest.mark.smoke
    def test_PayOrderGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/order/get"
        params = {"id": 15617637160}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
