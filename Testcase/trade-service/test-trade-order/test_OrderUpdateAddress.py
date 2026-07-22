import pytest
from config import ADMIN_URL


class TestOrderUpdateAddress:
    """修改订单收货地址"""

    @pytest.mark.smoke
    def test_OrderUpdateAddress(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/order/update-address"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
