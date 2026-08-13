import pytest
from config import ADMIN_URL


class Test_AppApiRecycleAppOrderPageStationClear:
    """APP站点清洁分页"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderPageStationClear(self, order_chain):
        chain, order_id, station_token, _ = order_chain
        r = chain._get(f"{ADMIN_URL}/admin-api/recycle/app-order/page-station-clear",
                       {"pageNo": 1, "pageSize": 10, "status": 10}, chain._b_headers(station_token))
        print(r)
