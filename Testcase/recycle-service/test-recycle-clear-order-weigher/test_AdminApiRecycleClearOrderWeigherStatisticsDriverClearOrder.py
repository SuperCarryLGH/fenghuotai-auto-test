import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherStatisticsDriverClearOrder:
    """称重员司机清运单统计"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherStatisticsDriverClearOrder(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/weigher/statistics-driver-clear-order"
        params = {"id": weigher_data['weigher']['order_id']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
