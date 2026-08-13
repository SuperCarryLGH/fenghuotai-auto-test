import pytest


class Test_AppApiRecycleAppOrderOrderWeighting:
    """APP订单称重"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderOrderWeighting(self, order_chain):
        chain, order_id, station_token, _ = order_chain
        chain.order_receive(order_id, station_token)
        item_id = chain.order_get_item_id(order_id, station_token)
        r = chain.order_weigh(order_id, item_id, station_token)
        print(r)
