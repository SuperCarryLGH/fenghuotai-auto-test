import pytest
from config import ADMIN_URL


class Test_AppApiRecycleAppOrderPageStation:
    """APP站点分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderPageStation(self, order_chain):
        chain, order_id, station_token, _ = order_chain
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-order/page-station",
                       {"pageNo": 1, "pageSize": 10}, chain._b_headers(station_token))
        print(r)
