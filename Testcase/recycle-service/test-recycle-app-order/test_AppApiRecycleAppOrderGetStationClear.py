import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderGetStationClear:
    """APP获取站点清洁"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderGetStationClear(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/get-station-clear"
        params = {"id": order_data['app_order']['order_id']}
        ok(api_session.get(url, params=params, headers=auth_headers))
