import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderReceive:
    """APP收货"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderReceive(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-order/receive"
        body = {"id": order_data['app_order']['order_id']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
