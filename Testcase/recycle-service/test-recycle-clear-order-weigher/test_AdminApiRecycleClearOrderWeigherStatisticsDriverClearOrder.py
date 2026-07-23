import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherStatisticsDriverClearOrder:
    """称重员司机清运单统计"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherStatisticsDriverClearOrder(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/statistics-driver-clear-order"
        params = {"driverId": weigher_data['weigher']['driver_id']}
        ok(api_session.get(url, params=params, headers=auth_headers))
