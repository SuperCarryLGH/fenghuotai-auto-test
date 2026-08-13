import pytest


class Test_AppApiRecycleAppOrderPayOrder:
    """APP支付订单"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderPayOrder(self, order_chain):
        chain, order_id, station_token, _ = order_chain
        chain.order_receive(order_id, station_token)
        item_id = chain.order_get_item_id(order_id, station_token)
        chain.order_weigh(order_id, item_id, station_token)
        r = chain.order_pay(order_id, station_token)
        print(r)
