import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderStationClearWeightStatistic:
    """APP站点清洁重量统计"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderStationClearWeightStatistic(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/station-clear-weight-statistic"
        params = {"id": order_data['app_order']['order_id']}
        ok(api_session.get(url, params=params, headers=auth_headers))
