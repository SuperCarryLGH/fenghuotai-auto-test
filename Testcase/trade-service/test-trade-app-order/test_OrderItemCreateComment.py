import pytest
from config import APP_URL


class TestOrderItemCreateComment:
    """创建交易订单项的评价"""

    @pytest.mark.smoke
    def test_OrderItemCreateComment(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/order/item/create-comment"
        body = {"id": "trade_app_order_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
