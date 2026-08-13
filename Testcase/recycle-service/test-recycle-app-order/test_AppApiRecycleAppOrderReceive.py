import pytest


class Test_AppApiRecycleAppOrderReceive:
    """APP收货（站点接单）"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderReceive(self, order_chain):
        chain, order_id, station_token, _ = order_chain
        r = chain.order_receive(order_id, station_token)
        print(r)
