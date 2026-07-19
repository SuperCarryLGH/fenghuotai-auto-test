import pytest
from config import ADMIN_URL


class TestPayOrderGetDetail:
    """获得支付订单详情"""

    @pytest.mark.smoke
    def test_PayOrderGetDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/order/get-detail"
        params = {"id": 15617637160}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
