import pytest
from config import ADMIN_URL


class TestOrderUpdateAddress:
    """修改订单收货地址"""

    @pytest.mark.smoke
    @pytest.mark.xfail(reason="dev 环境无法支付订单，订单状态为待付款，不允许修改地址")
    def test_OrderUpdateAddress(self, api_session, auth_headers, order_id):
        url = f"{ADMIN_URL}/admin-api/trade/order/update-address"
        body = {
            "id": order_id,
            "receiverName": "张三",
            "receiverMobile": "13800138000",
            "receiverAreaId": 7310,
            "receiverDetailAddress": "昆明市五华区测试地址",
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
