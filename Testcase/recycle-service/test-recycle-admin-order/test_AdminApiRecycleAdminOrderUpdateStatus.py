import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleAdminOrderUpdateStatus:
    """admin更新回收订单状态"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderUpdateStatus(self, order_chain, api_session, auth_headers, ok):
        chain, order_id, station_token, _ = order_chain
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/update-status"
        r = ok(api_session.put(url, json={"id": order_id, "status": 20}, headers=auth_headers))
        print(r)
